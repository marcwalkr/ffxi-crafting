import threading
import logging
import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
from abc import ABC, abstractmethod
from queue import Queue, Empty
from utils import TreeviewWithSort
from views import RecipeDetailPage
from controllers import RecipeController, CraftingController, ItemController
from database import Database

logger = logging.getLogger(__name__)


class RecipeListPage(ttk.Frame, ABC):
    """
    Abstract base class for a FFXI crafting recipe list page in a Tkinter application.
    Handles displaying and processing recipes in a treeview with multithreading.
    """

    def __init__(self, parent: tk) -> None:
        """
        Initialize the RecipeListPage.

        Args:
            parent (tkinter.Tk): The parent Tkinter application.
        """
        super().__init__(parent.notebook)
        self._parent = parent

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
        """Create and layout the widgets for the page."""
        self._parent.notebook.add(self, text=self.get_tab_text())
        self._create_action_button()
        self._create_progress_bar()
        self._create_treeview()

    def _create_action_button(self) -> None:
        """Create the action button for starting and stopping the process."""
        self.action_button = ttk.Button(self, text=self.action_button_text, command=self._toggle_process)
        self.action_button.pack(pady=10)

    def _create_progress_bar(self) -> None:
        """Create the progress bar for indicating processing status."""
        self._progress_bar = ttk.Progressbar(self, mode="indeterminate", length=300)
        self._progress_bar.pack_forget()

    def _create_treeview(self) -> None:
        """Create the treeview for displaying recipes."""
        self._treeview = TreeviewWithSort(self, columns=self.get_treeview_columns(), show="headings")
        self.configure_treeview(self._treeview)
        self._treeview.pack(padx=10, pady=10, expand=True, fill="both")
        self._treeview.bind("<Double-1>", self._show_recipe_details)
        self._treeview.bind("<Button-1>", self._on_treeview_click)

    @abstractmethod
    def get_tab_text(self) -> str:
        """Return the text for the tab."""
        pass

    @abstractmethod
    def get_treeview_columns(self) -> list[str]:
        """Return the columns for the treeview."""
        pass

    @abstractmethod
    def configure_treeview(self, treeview: ttk.Treeview) -> None:
        """Configure the treeview settings."""
        pass

    @abstractmethod
    def get_recipe_batch(self, batch_size: int, offset: int) -> list[any]:
        """
        Fetch a batch of recipes.

        Args:
            batch_size (int): The number of recipes to fetch.
            offset (int): The offset for pagination.

        Returns:
            list: A list of Recipe objects.
        """
        pass

    @abstractmethod
    def format_row(self, craft_result: dict) -> list[any]:
        """
        Format a row for the treeview based on the craft result.

        Args:
            craft_result (dict): The craft result to format.

        Returns:
            list: A list of values to display in the treeview.
        """
        pass

    def _toggle_process(self) -> None:
        """Toggle the process between start and cancel."""
        if self.action_button["text"] == self.action_button_text:
            self.start_process()
        else:
            self._cancel_process()

    def _show_recipe_details(self, event: tk.Event) -> None:
        """Show the details of the selected recipe in a new tab."""
        tree = event.widget
        if not tree.selection():
            return

        recipe_id = tree.selection()[0]
        recipe = self.recipe_controller.get_recipe(int(recipe_id))

        detail_page = RecipeDetailPage(self._parent, recipe)
        self._parent.notebook.add(detail_page, text=f"Recipe {recipe.result_name} Details")
        self._parent.notebook.select(detail_page)

    def _on_treeview_click(self, event: tk.Event) -> None:
        """Handle clicks on the treeview to clear selection if clicking on empty space or heading."""
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())

    def start_process(self) -> None:
        """Start the process of fetching and processing recipes."""
        self._cancel_event.clear()
        self.action_button["text"] = "Cancel"
        self._progress_bar.pack(pady=10, before=self._treeview)
        self._progress_bar.start()
        self._clear_treeview(self._treeview)

        self._init_executor()
        self._clear_insert_queue()

        self._query_thread = threading.Thread(target=self._fetch_and_process_batches)
        self._query_thread.start()

        self.after(100, self._check_insert_queue)

    def _cancel_process(self) -> None:
        """Cancel the ongoing process."""
        self._cancel_event.set()
        self.action_button["text"] = "Canceling..."
        self.action_button["state"] = "disabled"

    def _finish_process(self) -> None:
        """Finish the process and update the UI."""
        self._shutdown_executor()

    def _shutdown_executor(self) -> None:
        """Shutdown the thread pool executor."""
        if self._executor:
            self._executor.shutdown(wait=False)
            self._check_executor_shutdown()

    def _check_executor_shutdown(self) -> None:
        """Check if all futures are done and update the UI accordingly."""
        if all(f.done() for f in self._futures):
            self._finish_ui_update()
        else:
            self.after(100, self._check_executor_shutdown)

    def _finish_ui_update(self) -> None:
        """Update the UI after the process is finished."""
        self._progress_bar.stop()
        self._progress_bar.pack_forget()

        self.action_button["text"] = self.action_button_text
        self.action_button["state"] = "normal"

    def _fetch_and_process_batches(self) -> None:
        """Fetch and process batches of recipes in a separate thread."""
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

    def _process_batch(self, recipes: list[any]) -> None:
        """
        Process a batch of recipes.

        Args:
            recipes (list[Recipe]): The list of Recipe objects to process.
        """
        with Database() as db:
            item_controller = ItemController(db)
            crafting_controller = CraftingController(item_controller)

            for recipe in recipes:
                if self._cancel_event.is_set():
                    break
                self._process_single_recipe(recipe, crafting_controller)

    def _process_single_recipe(self, recipe: any, crafting_controller: CraftingController) -> None:
        """
        Process a single recipe.

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
        Default is True and subclasses can override.

        Args:
            craft_result (dict): The craft result to check.

        Returns:
            bool: True if the recipe should be displayed, False otherwise.
        """
        return True

    def _clear_treeview(self, treeview: ttk.Treeview) -> None:
        """Clear all items from the treeview."""
        for item in treeview.get_children():
            treeview.delete(item)

    def _insert_single_into_treeview(self, recipe_id: int, row: list[any]) -> None:
        """
        Insert a single row into the treeview.

        Args:
            recipe_id (int): The ID of the recipe to insert.
            row (list[any]): The row of values to insert.
        """
        self._treeview.insert("", "end", iid=recipe_id, values=row)

    def _init_executor(self) -> None:
        """Initialize the thread pool executor."""
        if self._executor:
            self._executor.shutdown(wait=False)
        self._executor = ThreadPoolExecutor(max_workers=self._max_threads)

    def _clear_insert_queue(self) -> None:
        """Clear the insert queue."""
        while not self._insert_queue.empty():
            try:
                self._insert_queue.get_nowait()
            except Empty:
                break
        self._insert_queue.queue.clear()

    def _check_insert_queue(self) -> None:
        """Check the insert queue and update the treeview."""
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
        """Cleanup resources and shutdown threads."""
        self._cancel_event.set()
        if self._executor:
            self._executor.shutdown(wait=False)
        if self._query_thread and self._query_thread.is_alive():
            self._query_thread.join(timeout=1)
