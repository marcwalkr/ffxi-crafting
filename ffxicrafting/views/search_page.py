import threading
import logging
import tkinter as tk
import traceback
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from queue import Queue, Empty
from config import SettingsManager
from controllers import RecipeController, CraftingController
from database import Database
from entities import Recipe
from utils import TreeviewWithSort, get_number_settings, create_number_settings
from views import RecipeDetailPage


logger = logging.getLogger(__name__)


class SearchPage(ttk.Frame):
    """
    A page for searching for profitable items to craft in FFXI.
    Handles filtering, simulating recipes, and displaying results in a treeview with multithreading.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """
        Initialize the SearchPage.
        Sets up the basic structure, database connections, and threading components.

        Args:
            parent (tk.Tk): The parent Tkinter application.
        """
        super().__init__(parent.notebook)
        self._parent = parent

        self._action_frame: ttk.Frame = None
        self._action_button: ttk.Button = None
        self._progress_bar: ttk.Progressbar = None
        self._treeview: TreeviewWithSort = None

        self._search_var: tk.StringVar = None
        self._search_entry: ttk.Entry = None

        self._filters_frame: ttk.Frame = None
        self._filters_button: ttk.Button = None
        self._filters_visible: bool = False
        self._settings: dict = SettingsManager.load_settings()

        self._num_threads: int = 20
        self._batch_size: int = 25

        self._executor: ThreadPoolExecutor = None
        self._recipe_queue: Queue = Queue()
        self._fetch_futures: list[Future] = []
        self._process_futures: list[Future] = []
        self._offset: int = 0

        self._offset_lock: threading.Lock = threading.Lock()
        self._cancel_event: threading.Event = threading.Event()

        self.create_widgets()

    def create_widgets(self) -> None:
        """
        Create and layout the widgets for the page.

        Adds the page to the notebook, creates the action frame, progress bar, and treeview.
        """
        self._parent.notebook.add(self, text="Search Items")
        self._create_action_frame()
        self._create_filters_frame()
        self._create_progress_bar()
        self._create_treeview()

    def _create_action_frame(self) -> None:
        """
        Create the search input and button within the input frame.
        """
        self._action_frame = ttk.Frame(self)
        self._action_frame.pack(pady=(10, 5))

        self._search_var = tk.StringVar()
        self._search_entry = ttk.Entry(self._action_frame, textvariable=self._search_var,
                                       font=("Helvetica", 14), width=20)
        self._search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self._search_entry.bind("<Return>", lambda event: self._toggle_process())

        self._action_button = ttk.Button(self._action_frame, text="Search", command=self._toggle_process)
        self._action_button.pack(side=tk.LEFT, padx=(0, 10))

        self._filters_button = ttk.Button(self._action_frame, text="Filters", command=self._toggle_filters)
        self._filters_button.pack(side=tk.LEFT, padx=(0, 10))

    def _create_filters_frame(self) -> None:
        """
        Create the filters frame containing threshold settings.

        This frame is initially hidden and can be toggled with the Filters button.
        It contains the Thresholds section with number input fields.
        """
        self._filters_frame = ttk.Frame(self)
        self._filters_frame.pack_forget()  # Initially hidden

        # Thresholds settings
        thresholds_frame = ttk.LabelFrame(self._filters_frame, text="Thresholds")
        thresholds_frame.pack(fill="x", padx=10, pady=(0, 5))

        thresholds_inner_frame = ttk.Frame(thresholds_frame)
        thresholds_inner_frame.pack(padx=5, pady=5)

        create_number_settings(thresholds_inner_frame, [
            ("Profit / Synth", 0),
            ("Profit / Storage", 0),
            ("Sell Frequency", 0)
        ], self._settings.get("thresholds", {}), orientation="horizontal")

    def _save_filter_settings(self) -> None:
        """
        Save the current filter settings to the application's configuration.

        This method retrieves the current values from the threshold input fields,
        updates the existing settings with these new values, and then saves the
        updated settings using the SettingsManager.
        """
        current_settings = SettingsManager.load_settings()
        new_settings = {
            "thresholds": get_number_settings(self._filters_frame.winfo_children()[0]),
        }
        current_settings.update(new_settings)
        SettingsManager.save_settings(current_settings)

    def _toggle_filters(self) -> None:
        """
        Toggle the visibility of the filters frame.

        If the filters are currently visible, this method hides them.
        If they are hidden, it displays them above the treeview.
        """
        if self._filters_visible:
            self._filters_frame.pack_forget()
            self._filters_visible = False
        else:
            self._filters_frame.pack(before=self._treeview)
            self._filters_visible = True

    def _create_progress_bar(self) -> None:
        """
        Create the progress bar for indicating processing status.

        Initializes an indeterminate progress bar, initially hidden from view.
        """
        self._progress_bar = ttk.Progressbar(self, mode="indeterminate", length=550)
        self._progress_bar.pack(pady=10)
        self._progress_bar.pack_forget()  # Hide it initially

    def _create_treeview(self) -> None:
        """
        Create the treeview for displaying recipes.

        Sets up the treeview with sortable columns and binds double-click and single-click events.
        """
        self._treeview = TreeviewWithSort(self, columns=self._get_treeview_columns(), show="headings")
        self._configure_treeview(self._treeview)
        self._treeview.pack(padx=10, pady=10, expand=True, fill="both")
        self._treeview.bind("<Double-1>", self._show_recipe_details)
        self._treeview.bind("<Button-1>", self._treeview.on_click)

    def _get_treeview_columns(self) -> list[str]:
        """
        Return the columns for the treeview.

        Returns:
            list[str]: A list of column identifiers for the treeview:
            ["nq", "hq", "levels", "ingredients"]
        """
        return ("nq", "hq", "levels", "ingredients")

    def _configure_treeview(self, treeview: ttk.Treeview) -> None:
        """
        Configure the treeview settings.
        Sets up column headings, text, and alignment for the search results treeview.

        Args:
            treeview (ttk.Treeview): The treeview to configure.
        """
        treeview.heading("nq", text="NQ")
        treeview.heading("hq", text="HQ")
        treeview.heading("levels", text="Craft Levels")
        treeview.heading("ingredients", text="Ingredients")
        treeview.column("levels", anchor=tk.CENTER)

    def _get_recipe_batch(self, recipe_controller: RecipeController, batch_size: int, offset: int) -> list[Recipe]:
        """
        Fetch a batch of recipes based on the user's search query.

        Args:
            recipe_controller (RecipeController): The recipe controller to use.
            batch_size (int): The number of recipes to fetch.
            offset (int): The offset for pagination.

        Returns:
            list: A list of Recipe objects matching the search query,
                  fetched from RecipeController.
        """
        return recipe_controller.search_recipe(self._search_var.get(), batch_size, offset)

    def _format_row(self, craft_result: dict[str, any]) -> list[str]:
        """
        Format a row for the treeview based on the craft result.

        Args:
            craft_result (dict[str, any]): The craft result to format.

        Returns:
            list[str]: A list of formatted strings for the treeview:
            [0] NQ result: Formatted string of the normal quality result
            [1] HQ results: Formatted string of the high quality results
            [2] Craft levels: Formatted string of the required crafting levels
            [3] Ingredients: Formatted string of the required ingredients
        """
        recipe = craft_result["crafter"].recipe

        return [
            recipe.get_formatted_nq_result(),
            recipe.get_formatted_hq_results(),
            recipe.get_formatted_levels_string(),
            recipe.get_formatted_ingredient_names()
        ]

    def _toggle_process(self) -> None:
        """
        Toggle between starting and canceling the search process.

        If the search is not running, this method saves the current filter settings,
        collapses the filters if they're visible, and starts the search process.
        If the search is already running, it cancels the process.
        """
        if self._action_button["text"] == "Search":
            self._save_filter_settings()
            if self._filters_visible:
                self._toggle_filters()
            self._start_process()
        else:
            self._cancel_process()

    def _show_recipe_details(self, event: tk.Event) -> None:
        """
        Show the details of the selected recipe in a new tab.
        Opens a new RecipeDetailPage for the selected recipe.

        Args:
            event (tk.Event): The event triggered by double-clicking a recipe.
        """
        tree = event.widget
        if not tree.selection():
            return

        recipe_id = tree.selection()[0]
        profit_data = CraftingController.get_profit_data(int(recipe_id))

        detail_page = RecipeDetailPage(self._parent, profit_data)
        self._parent.notebook.add(detail_page, text=f"Recipe {profit_data.recipe.result_name} Details")
        self._parent.notebook.select(detail_page)

    def _start_process(self) -> None:
        """
        Start the process of fetching and processing recipes.

        Initializes the UI for processing, sets up threading, and begins fetching recipes.
        """
        # Reset state
        self._cancel_event.clear()
        self._offset = 0

        # Clear and prepare data structures
        self._recipe_queue = Queue()
        self._fetch_futures = []

        # Update UI
        self._action_button["text"] = "Cancel"
        self._progress_bar.pack(pady=10, before=self._treeview)
        self._progress_bar.start()
        self._treeview.clear()

        # Start executor in a new thread to avoid blocking the main thread
        threading.Thread(target=self._start_executor, daemon=True).start()

    def _cancel_process(self) -> None:
        """
        Cancel the ongoing process.

        Sets the cancel event, disables the button and updates the button text to "Canceling...".
        """
        self._cancel_event.set()
        self._action_button["text"] = "Canceling..."
        self._action_button["state"] = "disabled"

    def _finish_process(self) -> None:
        """
        Finish the process and clean up resources.

        Shuts down the executor and updates the UI to reflect the completion of the process.
        """
        if self._executor:
            self._executor.shutdown(wait=False)

        # Update UI
        self._progress_bar.stop()
        self._progress_bar.pack_forget()
        self._action_button["text"] = "Search"
        self._action_button["state"] = "normal"

    def _start_executor(self) -> None:
        """
        Initialize and start the ThreadPoolExecutor.

        Creates separate threads for fetching and processing recipes, and submits a task to wait for completion.
        """
        self._executor = ThreadPoolExecutor(max_workers=self._num_threads)
        fetch_futures = [self._executor.submit(self._fetch_recipes) for _ in range(self._num_threads // 2)]
        process_futures = [self._executor.submit(self._process_recipes) for _ in range(self._num_threads // 2)]

        all_futures = fetch_futures + process_futures
        self._executor.submit(self._wait_for_completion, all_futures)

    def _fetch_recipes(self) -> None:
        """
        Fetch recipes in batches and add them to the recipe queue.

        Continues fetching until there are no more recipes or the process is canceled.
        Adds a None value to the queue to signal completion.
        """
        try:
            while not self._cancel_event.is_set():
                with self._offset_lock:
                    offset = self._offset
                    self._offset += self._batch_size

                with Database() as db:
                    recipe_controller = RecipeController(db)
                    recipes = self._get_recipe_batch(recipe_controller, self._batch_size, offset)

                    if not recipes:
                        break

                    for recipe in recipes:
                        self._recipe_queue.put(recipe)
        except Exception:
            traceback.print_exc()

        self._recipe_queue.put(None)  # Signal this fetch thread is done

    def _process_recipes(self) -> None:
        """
        Process recipes from the recipe queue.

        Continuously retrieves recipes from the queue and processes them
        until receiving a None value or the process is canceled.
        """
        try:
            while True:
                try:
                    recipe = self._recipe_queue.get(timeout=1)
                    if recipe is None:
                        break
                    self._process_single_recipe(recipe)
                except Empty:
                    if self._cancel_event.is_set():
                        break
        except Exception:
            traceback.print_exc()

    def _process_single_recipe(self, recipe: Recipe) -> None:
        """
        Process a single recipe.
        Simulates the craft and adds the result to the insert queue if it should be displayed.

        Args:
            recipe (Recipe): The Recipe object to process.
        """
        if self._cancel_event.is_set():
            return

        craft_result = CraftingController.simulate_craft(recipe)

        if not craft_result:
            return

        if self._should_display_recipe(craft_result):
            row = self._format_row(craft_result)
            self._insert_single_into_treeview(recipe.id, row)

    def _wait_for_completion(self, futures):
        """
        Wait for all futures to complete and finish the process.

        Args:
            futures (list): List of Future objects to wait for.

        Calls _finish_process on the main thread after all futures are completed.
        """
        for future in as_completed(futures):
            future.result()  # This will raise any exceptions that occurred

        self.after(0, self._finish_process)

    def _should_display_recipe(self, craft_result: dict) -> bool:
        """
        Determine if a recipe should be displayed in the treeview.

        Args:
            craft_result (dict): The craft result to check.

        Returns:
            bool: True if the recipe should be displayed, False otherwise.
        """
        return True

    def _insert_single_into_treeview(self, recipe_id: int, row: list[any]) -> None:
        """
        Insert a single row into the treeview.

        Args:
            recipe_id (int): The ID of the recipe to insert.
            row (list[any]): The row of values to insert.
        """
        self._treeview.insert("", "end", iid=recipe_id, values=row)

    def cleanup(self) -> None:
        """
        Cleanup resources and shutdown threads.

        Should be called when the page is being closed or the application is shutting down.
        """
        self._cancel_event.set()
