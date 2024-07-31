import threading
import logging
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor, as_completed
from abc import ABC, abstractmethod
from queue import Queue, Empty
from utils import TreeviewWithSort
from views import RecipeDetailPage
from controllers import RecipeController, CraftingController, ItemController
from database import Database

logger = logging.getLogger(__name__)


class RecipeListPage(ttk.Frame, ABC):
    def __init__(self, parent):
        super().__init__(parent.notebook)
        self.parent = parent
        self.recipe_db = Database()
        self.recipe_controller = RecipeController(self.recipe_db)

        self.query_thread = None
        self.max_threads = 15
        self.executor = None
        self.insert_queue = Queue()
        self.cancel_event = threading.Event()

        self.create_widgets()

    def create_widgets(self):
        self.parent.notebook.add(self, text=self.get_tab_text())
        self.create_action_button()
        self.create_progress_bar()
        self.create_treeview()

    def create_action_button(self):
        self.action_button = ttk.Button(self, text=self.action_button_text, command=self.toggle_process)
        self.action_button.pack(pady=10)

    def create_progress_bar(self):
        self.progress_bar = ttk.Progressbar(self, mode="indeterminate", length=300)
        self.progress_bar.pack_forget()

    def create_treeview(self):
        self.treeview = TreeviewWithSort(self, columns=self.get_treeview_columns(), show="headings")
        self.configure_treeview(self.treeview)
        self.treeview.pack(padx=10, pady=10, expand=True, fill="both")
        self.treeview.bind("<Double-1>", self.show_recipe_details)
        self.treeview.bind("<Button-1>", self.on_treeview_click)

    @abstractmethod
    def get_tab_text(self):
        pass

    @abstractmethod
    def get_treeview_columns(self):
        pass

    @abstractmethod
    def configure_treeview(self, treeview):
        pass

    @abstractmethod
    def get_recipe_batch(self, batch_size, offset):
        pass

    @abstractmethod
    def format_row(self, craft_result):
        pass

    def toggle_process(self):
        if self.action_button["text"] == self.action_button_text:
            self.start_process()
        else:
            self.cancel_process()

    def show_recipe_details(self, event):
        tree = event.widget
        if not tree.selection():
            return

        recipe_id = tree.selection()[0]
        recipe = self.recipe_controller.get_recipe(int(recipe_id))

        detail_page = RecipeDetailPage(self.parent, recipe)
        self.parent.notebook.add(detail_page, text=f"Recipe {recipe.result_name} Details")
        self.parent.notebook.select(detail_page)

    def on_treeview_click(self, event):
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())

    def start_process(self):
        self.cancel_event.clear()
        self.action_button["text"] = "Cancel"
        self.progress_bar.pack(pady=10, before=self.treeview)
        self.progress_bar.start()
        self.clear_treeview(self.treeview)

        self.init_executor()
        self.clear_insert_queue()

        self.query_thread = threading.Thread(target=self.fetch_and_process_batches)
        self.query_thread.start()

        self.after(100, self.check_insert_queue)

    def cancel_process(self):
        self.cancel_event.set()
        self.action_button["text"] = "Canceling..."
        self.action_button["state"] = "disabled"

    def finish_process(self):
        threading.Thread(target=self.shutdown_executor, daemon=True).start()

    def shutdown_executor(self):
        if self.executor:
            self.executor.shutdown(wait=True)
        self.after(0, self.finish_ui_update)

    def finish_ui_update(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

        self.action_button["text"] = self.action_button_text
        self.action_button["state"] = "normal"

    def fetch_and_process_batches(self):
        batch_size = 25
        offset = 0
        futures = []

        while not self.cancel_event.is_set():
            recipes = self.get_recipe_batch(batch_size, offset)

            if not recipes:
                break

            future = self.executor.submit(self.process_batch, recipes)
            futures.append(future)

            offset += batch_size

        # Wait for all processing to complete
        for future in as_completed(futures):
            if self.cancel_event.is_set():
                break

        # Close the connection used for querying recipes
        self.recipe_db.close_connection()

        # Signal that processing is complete
        self.insert_queue.put(("DONE", None))

    def process_batch(self, recipes):
        db = Database()
        try:
            item_controller = ItemController(db)
            crafting_controller = CraftingController(item_controller)

            for recipe in recipes:
                if self.cancel_event.is_set():
                    break
                self.process_single_recipe(recipe, crafting_controller)
        finally:
            db.close_connection()

    def process_single_recipe(self, recipe, crafting_controller):
        if self.cancel_event.is_set():
            return

        craft_result = crafting_controller.simulate_craft(recipe)

        if not craft_result:
            return

        if self.should_display_recipe(craft_result):
            row = self.format_row(craft_result)
            self.insert_queue.put((recipe.id, row))

    def should_display_recipe(self, craft_result):
        # Default to True, subclasses can override
        return True

    def clear_treeview(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

    def insert_single_into_treeview(self, recipe_id, row):
        self.treeview.insert("", "end", iid=recipe_id, values=row)

    def init_executor(self):
        if self.executor:
            self.executor.shutdown(wait=False)
        self.executor = ThreadPoolExecutor(max_workers=self.max_threads)

    def clear_insert_queue(self):
        while not self.insert_queue.empty():
            try:
                self.insert_queue.get_nowait()
            except Empty:
                break
        self.insert_queue.queue.clear()

    def check_insert_queue(self):
        try:
            while True:
                recipe_id, row = self.insert_queue.get_nowait()

                if recipe_id == "DONE":
                    self.finish_process()
                    return

                self.insert_single_into_treeview(recipe_id, row)
        except Empty:
            pass

        self.after(100, self.check_insert_queue)

    def on_close(self):
        self.cancel_event.set()
