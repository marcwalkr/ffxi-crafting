import threading
import logging
import tkinter as tk
import traceback
from tkinter import ttk
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
    Handles searching, simulating recipes, filtering, and displaying results in a treeview.
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

        self._recipe_queue: Queue[Recipe] = Queue()
        self._insert_queue: Queue[tuple[int, list[any]]] = Queue()
        self._cancel_event: threading.Event = threading.Event()
        self._producer_thread: threading.Thread = None
        self._consumer_thread: threading.Thread = None

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
        thresholds_frame = ttk.LabelFrame(self._filters_frame)
        thresholds_frame.pack(fill="x", padx=10, pady=(0, 5))

        thresholds_inner_frame = ttk.Frame(thresholds_frame)
        thresholds_inner_frame.pack(padx=5, pady=5)

        create_number_settings(thresholds_inner_frame, [
            ("Profit / Synth", 0),
            ("Profit / Storage", 0),
            ("Sell Frequency", 0)
        ], self._settings.get("thresholds", {}), orientation="horizontal")

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
        columns = ["nq", "hq", "levels", "ingredients"]
        self._treeview = TreeviewWithSort(self, columns=columns, show="headings")
        self._configure_treeview(self._treeview)
        self._treeview.pack(padx=10, pady=10, expand=True, fill="both")
        self._treeview.bind("<Double-1>", self._show_recipe_details)
        self._treeview.bind("<Button-1>", self._treeview.on_click)

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

    def _start_process(self) -> None:
        """
        Start the process of fetching and processing recipes.

        Initializes the UI for processing, sets up threading, and begins fetching and processing recipes.
        """
        self._cancel_event.clear()
        self._action_button["text"] = "Cancel"
        self._progress_bar.pack(pady=10, before=self._treeview)
        self._progress_bar.start()
        self._treeview.clear()

        self._producer_thread = threading.Thread(target=self._produce_recipes, daemon=True)
        self._producer_thread.start()

        self._consumer_thread = threading.Thread(target=self._consume_recipes, daemon=True)
        self._consumer_thread.start()

        self.after(100, self._check_insert_queue)

    def _produce_recipes(self) -> None:
        """
        Fetch recipes and add them to the recipe queue.

        This method runs in a separate thread. It queries the database for recipes
        based on the search criteria and puts them into the recipe queue for processing.
        If cancelled, it will stop fetching recipes and signal the end of the queue.
        """
        try:
            with Database() as db:
                recipe_controller = RecipeController(db)
                recipes = recipe_controller.search_recipe(self._search_var.get())

                for recipe in recipes:
                    if self._cancel_event.is_set():
                        break
                    self._recipe_queue.put(recipe)

        except Exception:
            traceback.print_exc()
        finally:
            self._recipe_queue.put(None)  # Signal end of recipes

    def _consume_recipes(self) -> None:
        """
        Process recipes from the recipe queue.

        This method runs in a separate thread. It continuously takes recipes from the queue,
        simulates the craft, and if the recipe should be displayed, formats the result and
        adds it to the insert queue. It will stop when it receives a None value (end of queue)
        or when cancelled.
        """
        while not self._cancel_event.is_set():
            try:
                recipe = self._recipe_queue.get(timeout=0.1)
                if recipe is None:
                    break
                craft_result = CraftingController.simulate_craft(recipe)
                if craft_result and self._should_display_recipe(craft_result):
                    row = self._format_row(craft_result)
                    self._insert_queue.put((recipe.id, row))
            except Empty:
                continue
            except Exception:
                traceback.print_exc()

        self._insert_queue.put(None)  # Signal that processing is complete

    def _check_insert_queue(self) -> None:
        """
        Check the insert queue for new results and insert them into the treeview.

        This method runs on the main thread. It processes items from the insert queue
        and adds them to the treeview. If it receives a None value, it signals that
        processing is complete and calls _finish_process.
        """
        try:
            while True:
                item = self._insert_queue.get_nowait()
                if item is None:
                    self._finish_process()
                    return
                recipe_id, row = item
                self._insert_single_into_treeview(recipe_id, row)
        except Empty:
            pass

        self.after(100, self._check_insert_queue)

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
        Clean up after the recipe processing is complete or cancelled.

        This method stops all threads, clears the queues, resets the UI elements,
        and prepares the page for a new search.
        """
        self._cancel_event.set()
        if self._consumer_thread:
            self._consumer_thread.join()
            self._consumer_thread = None
        if self._producer_thread:
            self._producer_thread.join()
            self._producer_thread = None

        # Clear queues
        while not self._recipe_queue.empty():
            self._recipe_queue.get()
        while not self._insert_queue.empty():
            self._insert_queue.get()

        self._progress_bar.stop()
        self._progress_bar.pack_forget()
        self._action_button["text"] = "Search"
        self._action_button["state"] = "normal"

    def _insert_single_into_treeview(self, recipe_id: int, row: list[any]) -> None:
        """
        Insert a single row into the treeview.

        Args:
            recipe_id (int): The ID of the recipe to insert.
            row (list[any]): The row of values to insert.
        """
        self._treeview.insert("", "end", iid=recipe_id, values=row)

    def _should_display_recipe(self, craft_result: dict) -> bool:
        """
        Determine if a recipe should be displayed in the treeview.

        Args:
            craft_result (dict): The craft result to check.

        Returns:
            bool: True if the recipe should be displayed, False otherwise.
        """
        return True

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
        skills = SettingsManager.get_craft_skills()
        cache_key = (int(recipe_id), *skills)
        simulation_data = CraftingController.get_simulation_data(cache_key)

        detail_page = RecipeDetailPage(self._parent, simulation_data)
        self._parent.notebook.add(detail_page, text=f"Recipe {simulation_data.recipe.result_name} Details")
        self._parent.notebook.select(detail_page)

    def cleanup(self) -> None:
        """
        Sets the cancel event to let the process finish.

        Should be called when the page is being closed or the application is shutting down.
        """
        self._cancel_event.set()
