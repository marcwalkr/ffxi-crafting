import threading
import logging
import tkinter as tk
import traceback
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from queue import Queue, Empty
from abc import ABC, abstractmethod
from controllers import RecipeController, CraftingController, ItemController
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

        self._recipe_db: Database = Database()
        self.recipe_controller: RecipeController = RecipeController(self._recipe_db)

        self._max_threads: int = 15
        self._query_thread: threading.Thread = None
        self._executor: ThreadPoolExecutor = None
        self._insert_queue: Queue = Queue()
        self._futures: list[Future] = []
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
        self._progress_bar = ttk.Progressbar(self, mode="indeterminate", length=500)
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
    def get_recipe_batch(self, batch_size: int, offset: int) -> list[Recipe]:
        """
        Fetch a batch of recipes.
        Implement this method to retrieve recipes from the database or other source.

        Args:
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
        recipe = self.recipe_controller.get_recipe(int(recipe_id))

        detail_page = RecipeDetailPage(self._parent, recipe)
        self._parent.notebook.add(detail_page, text=f"Recipe {recipe.result_name} Details")
        self._parent.notebook.select(detail_page)

    def start_process(self) -> None:
        """
        Start the process of fetching and processing recipes.

        Initializes the UI for processing, sets up threading, and begins fetching recipes.
        """
        self._cancel_event.clear()
        self.action_button["text"] = "Cancel"
        self._progress_bar.pack(pady=10, before=self._treeview)
        self._progress_bar.start()
        self._treeview.clear()

        self._init_executor()
        self._clear_insert_queue()

        self._query_thread = threading.Thread(target=self._fetch_and_process_batches)
        self._query_thread.start()

        self.after(100, self._check_insert_queue)

    def _cancel_process(self) -> None:
        """
        Cancel the ongoing process.

        Sets the cancel event and updates the UI to reflect the cancellation.
        """
        self._cancel_event.set()
        self.action_button["text"] = "Canceling..."
        self.action_button["state"] = "disabled"

    def _finish_process(self) -> None:
        """
        Finish the process and update the UI.

        Shuts down the executor and updates the UI to reflect process completion.
        """
        self._shutdown_executor()

    def _shutdown_executor(self) -> None:
        """
        Shutdown the thread pool executor.

        Initiates a non-blocking shutdown of the executor.
        """
        if self._executor:
            self._executor.shutdown(wait=False)
            self._check_executor_shutdown()

    def _check_executor_shutdown(self) -> None:
        """
        Check if all futures are done and update the UI accordingly.

        Recursively checks until all futures are complete, then calls _finish_ui_update.
        """
        if all(f.done() for f in self._futures):
            self._finish_ui_update()
        else:
            self.after(100, self._check_executor_shutdown)

    def _finish_ui_update(self) -> None:
        """
        Update the UI after the process is finished.

        Resets the progress bar and action button to their initial states.
        """
        self._progress_bar.stop()
        self._progress_bar.pack_forget()

        self.action_button["text"] = self.action_button_text
        self.action_button["state"] = "normal"

    def _fetch_and_process_batches(self) -> None:
        """
        Fetch and process batches of recipes in a separate thread.

        Continuously fetches batches of recipes and submits them for processing
        until all recipes are processed or cancellation is requested.
        """
        batch_size = 25
        offset = 0
        self._futures = []

        try:
            while not self._cancel_event.is_set():
                recipes = self.get_recipe_batch(batch_size, offset)

                if not recipes:
                    break

                try:
                    future = self._executor.submit(self._process_batch, recipes)
                    self._futures.append(future)
                except RuntimeError:
                    # Executor is shutting down, break the loop
                    break

                offset += batch_size

            # Wait for all processing to complete
            for future in as_completed(self._futures):
                if self._cancel_event.is_set():
                    break

        finally:
            # Close the connection used for querying recipes
            self._recipe_db.close_connection()

            # Signal that processing is complete
            self._insert_queue.put(("DONE", None))

    def _process_batch(self, recipes: list[Recipe]) -> None:
        """
        Process a batch of recipes.

        Args:
            recipes (list[Recipe]): The list of Recipe objects to process.
        """
        try:
            with Database() as db:
                item_controller = ItemController(db)
                crafting_controller = CraftingController(item_controller)

                for recipe in recipes:
                    if self._cancel_event.is_set():
                        break
                    self._process_single_recipe(recipe, crafting_controller)
        except Exception:
            traceback.print_exc()

    def _process_single_recipe(self, recipe: Recipe, crafting_controller: CraftingController) -> None:
        """
        Process a single recipe.
        Simulates the craft and adds the result to the insert queue if it should be displayed.

        Args:
            recipe (Recipe): The Recipe object to process.
            crafting_controller (CraftingController): The CraftingController object to use.
        """
        if self._cancel_event.is_set():
            return

        craft_result = crafting_controller.simulate_craft(recipe)

        if not craft_result:
            return

        if self.should_display_recipe(craft_result):
            row = self.format_row(craft_result)
            self._insert_queue.put((recipe.id, row))

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

    def _init_executor(self) -> None:
        """
        Initialize the thread pool executor.

        Shuts down any existing executor and creates a new one with max_workers threads.
        """
        if self._executor:
            self._executor.shutdown(wait=False)
        self._executor = ThreadPoolExecutor(max_workers=self._max_threads)

    def _clear_insert_queue(self) -> None:
        """
        Clear the insert queue.

        Removes all pending items from the insert queue.
        """
        while not self._insert_queue.empty():
            try:
                self._insert_queue.get_nowait()
            except Empty:
                break
        self._insert_queue.queue.clear()

    def _check_insert_queue(self) -> None:
        """
        Check the insert queue and update the treeview.

        Processes items in the insert queue, adding them to the treeview.
        Schedules itself to run again after a short delay if processing is not complete.
        """
        try:
            while True:
                recipe_id, row = self._insert_queue.get_nowait()

                if recipe_id == "DONE":
                    self._finish_process()
                    return

                self._insert_single_into_treeview(recipe_id, row)
        except Empty:
            pass

        self.after(100, self._check_insert_queue)

    def cleanup(self) -> None:
        """
        Cleanup resources and shutdown threads.

        Should be called when the page is being closed or the application is shutting down.
        """
        self._cancel_event.set()
        if self._executor:
            self._executor.shutdown(wait=False)
        if self._query_thread and self._query_thread.is_alive():
            self._query_thread.join(timeout=1)
