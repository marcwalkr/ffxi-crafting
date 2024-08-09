import threading
import logging
import tkinter as tk
import traceback
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from queue import Queue, Empty
from abc import ABC, abstractmethod
from controllers import RecipeController, CraftingController
from database import Database
from entities import Recipe
from utils import TreeviewWithSort
from views import RecipeDetailPage


logger = logging.getLogger(__name__)


class RecipeListPage(ttk.Frame, ABC):
    """
    Abstract base class for a FFXI crafting recipe list page in a Tkinter application.
    Handles displaying and processing recipes in a treeview with multithreading.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """
        Initialize the RecipeListPage.
        Sets up the basic structure, database connections, and threading components.

        Args:
            parent (tk.Tk): The parent Tkinter application.
        """
        super().__init__(parent.notebook)
        self._parent = parent

        self.action_frame: ttk.Frame = None
        self.action_button: ttk.Button = None
        self._progress_bar: ttk.Progressbar = None
        self._treeview: TreeviewWithSort = None
        self.action_button_text: str

        # Initialize a recipe controller instance for quickly fetching the recipe on treeview item click
        self._recipe_controller: RecipeController = RecipeController(Database())

        self._num_threads: int = 30
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
        self._parent.notebook.add(self, text=self.get_tab_text())
        self.create_action_frame()
        self._create_progress_bar()
        self._create_treeview()

    def create_action_frame(self) -> None:
        """
        Create a frame for action-related widgets (e.g., buttons, entry fields).

        This method can be overridden in subclasses to customize the action area.
        """
        self.action_frame = ttk.Frame(self)
        self.action_frame.pack(pady=10)
        self._create_action_button()

    def _create_action_button(self) -> None:
        """
        Create the action button for starting and stopping the process.

        The button text is set from self.action_button_text and toggles the process on click.
        """
        self.action_button = ttk.Button(self.action_frame, text=self.action_button_text, command=self._toggle_process)
        self.action_button.pack()

    def _create_progress_bar(self) -> None:
        """
        Create the progress bar for indicating processing status.

        Initializes an indeterminate progress bar, initially hidden from view.
        """
        self._progress_bar = ttk.Progressbar(self, mode="indeterminate", length=400)
        self._progress_bar.pack_forget()

    def _create_treeview(self) -> None:
        """
        Create the treeview for displaying recipes.

        Sets up the treeview with sortable columns and binds double-click and single-click events.
        """
        self._treeview = TreeviewWithSort(self, columns=self.get_treeview_columns(), show="headings")
        self.configure_treeview(self._treeview)
        self._treeview.pack(padx=10, pady=10, expand=True, fill="both")
        self._treeview.bind("<Double-1>", self._show_recipe_details)
        self._treeview.bind("<Button-1>", self._treeview.on_click)

    @abstractmethod
    def get_tab_text(self) -> str:
        """
        Return the text for the tab.

        Returns:
            str: The text to be displayed on the tab for this page.
        """
        pass

    @abstractmethod
    def get_treeview_columns(self) -> list[str]:
        """
        Return the columns for the treeview.

        Returns:
            list[str]: A list of column identifiers for the treeview.
        """
        pass

    @abstractmethod
    def configure_treeview(self, treeview: ttk.Treeview) -> None:
        """
        Configure the treeview settings.
        Implement this method to set up column headings, widths, and other treeview properties.

        Args:
            treeview (ttk.Treeview): The treeview to configure.
        """
        pass

    @abstractmethod
    def get_recipe_batch(self, recipe_controller: RecipeController, batch_size: int, offset: int) -> list[Recipe]:
        """
        Fetch a batch of recipes.
        Implement this method to retrieve recipes from the database or other source.

        Args:
            recipe_controller (RecipeController): The recipe controller to use.
            batch_size (int): The number of recipes to fetch.
            offset (int): The offset for pagination.

        Returns:
            list: A list of Recipe objects.
        """
        pass

    @abstractmethod
    def format_row(self, craft_result: dict[str, any]) -> list[any]:
        """
        Format a row for the treeview based on the craft result.
        Implement this method to convert a craft result into a list of values for the treeview.

        Args:
            craft_result (dict[str, any]): The craft result to format.

        Returns:
            list: A list of values to display in the treeview.
        """
        pass

    def _toggle_process(self) -> None:
        """
        Toggle the process between start and cancel.

        Starts the process if it's not running, or cancels it if it is.
        """
        if self.action_button["text"] == self.action_button_text:
            self.start_process()
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
        recipe = self._recipe_controller.get_recipe(int(recipe_id))

        detail_page = RecipeDetailPage(self._parent, recipe)
        self._parent.notebook.add(detail_page, text=f"Recipe {recipe.result_name} Details")
        self._parent.notebook.select(detail_page)

    def start_process(self) -> None:
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
        self.action_button["text"] = "Cancel"
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
        self.action_button["text"] = "Canceling..."
        self.action_button["state"] = "disabled"

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
        self.action_button["text"] = self.action_button_text
        self.action_button["state"] = "normal"

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
                    recipes = self.get_recipe_batch(recipe_controller, self._batch_size, offset)

                    if not recipes:
                        break

                    for recipe in recipes:
                        self._recipe_queue.put(recipe)
        except Exception as e:
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
        except Exception as e:
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

        crafting_controller = CraftingController(recipe)
        craft_result = crafting_controller.simulate_craft()

        if not craft_result:
            return

        if self.should_display_recipe(craft_result):
            row = self.format_row(craft_result)
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

    def should_display_recipe(self, craft_result: dict) -> bool:
        """
        Determine if a recipe should be displayed in the treeview.
        Default implementation always returns True. Override in subclasses for custom filtering.

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
