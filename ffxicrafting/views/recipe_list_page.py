import threading
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import ttk
from queue import Queue, Empty
from abc import ABC
from utils import TreeviewWithSort
from views import RecipeDetailPage
from database import Database
from controllers import RecipeController, CraftingController, ItemController

logger = logging.getLogger(__name__)


class RecipeListPage(ttk.Frame, ABC):
    def __init__(self, parent):
        super().__init__(parent.notebook)
        self.parent = parent
        self.recipe_controller = RecipeController()

        self.queue = Queue()
        self.executor = None
        self.cancel_event = threading.Event()
        self.process_thread = None
        self.active_db_connections = set()

        self.create_widgets()
        self.after(100, self.check_queue)

    def create_widgets(self):
        self.parent.notebook.add(self, text=self.get_tab_text())
        self.create_action_button()
        self.create_progress_bar()
        self.create_treeview()

    def get_tab_text(self):
        raise NotImplementedError("Subclasses must implement get_tab_text()")

    def create_action_button(self):
        self.action_button = ttk.Button(self, text=self.action_button_text, command=self.start_process)
        self.action_button.pack(pady=10)

    def create_progress_bar(self):
        self.progress_bar = ttk.Progressbar(self, mode='indeterminate', length=300)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget()

    def create_treeview(self):
        self.treeview = TreeviewWithSort(self, columns=self.get_treeview_columns(), show="headings")
        self.configure_treeview(self.treeview)
        self.treeview.pack(padx=10, pady=10, expand=True, fill="both")
        self.treeview.bind("<Double-1>", self.show_recipe_details)
        self.treeview.bind("<Button-1>", self.on_treeview_click)

    def get_treeview_columns(self):
        raise NotImplementedError("Subclasses must implement get_treeview_columns()")

    def configure_treeview(self, treeview):
        raise NotImplementedError("Subclasses must implement configure_treeview()")

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
        self.clear_treeview(self.treeview)
        self.show_progress()

        self.cancel_event.clear()
        self.show_cancel_button()

        self.executor = ThreadPoolExecutor(max_workers=15)
        threading.Thread(target=self.process_recipes, daemon=True).start()

    def clear_treeview(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

    def show_progress(self):
        self.progress_bar.pack(pady=10, before=self.treeview)
        self.progress_bar.start()

    def show_cancel_button(self):
        self.action_button.config(text="Cancel", command=self.cancel_process)

    def process_recipes(self):
        try:
            futures = []
            offset = 0
            search_finished = False

            while not self.cancel_event.is_set() and not search_finished:
                logger.debug(f"Fetching batch at offset {offset}")
                batch = self.get_recipe_batch(25, offset)

                if len(batch) < 25:
                    logger.info(f"Processing last batch: {len(batch)} recipes")
                    search_finished = True

                if batch:
                    futures.append(self.executor.submit(self.process_batch, batch))

                offset += 25

            for future in as_completed(futures):
                if self.cancel_event.is_set():
                    break
                try:
                    future.result(timeout=0.1)
                except Exception as e:
                    logger.error(f"Error processing batch: {e}")
        except Exception as e:
            logger.error(f"Error processing recipes: {e}")
        finally:
            logger.debug("Finished processing recipes, queueing cleanup")
            self.queue.put(self.cleanup)

    def get_recipe_batch(self, batch_size, offset):
        raise NotImplementedError("Subclasses must implement get_recipe_batch()")

    def process_batch(self, recipes):
        db = Database()
        self.active_db_connections.add(db)
        try:
            item_controller = ItemController(db)
            crafting_controller = CraftingController(item_controller)
            for recipe in recipes:
                if self.cancel_event.is_set():
                    break
                try:
                    self.process_single_recipe(recipe, crafting_controller)
                except Exception as e:
                    logger.error(f"Error processing recipe {recipe.id}: {e}")
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
        finally:
            db.close()
            self.active_db_connections.discard(db)

    def process_finished(self):
        logger.debug("Process finished")
        self.hide_progress()
        self.show_action_button()

    def hide_progress(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

    def show_action_button(self):
        self.action_button.config(text=self.action_button_text, command=self.start_process, state="normal")

    def process_single_recipe(self, recipe, crafting_controller):
        if self.cancel_event.is_set():
            return

        craft_result = crafting_controller.simulate_craft(recipe)

        if not craft_result:
            return

        if self.should_display_recipe(craft_result):
            row = self.format_row(craft_result)
            self.queue.put((recipe.id, row))

    def should_display_recipe(self, craft_result):
        # Default to True, subclasses can override
        return True

    def format_row(self, craft_result):
        raise NotImplementedError("Subclasses must implement format_row()")

    def insert_single_into_treeview(self, recipe_id, row):
        self.treeview.insert("", "end", iid=recipe_id, values=row)

    def check_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                if callable(task):
                    task()
                else:
                    recipe_id, row = task
                    self.insert_single_into_treeview(recipe_id, row)
        except Empty:
            pass
        finally:
            self.after(100, self.check_queue)

    def cancel_process(self):
        logger.debug("Cancellation requested")
        self.cancel_event.set()
        self.action_button.config(text="Canceling...", state="disabled")
        self.after(100, self.cleanup)

    def wait_for_cancellation(self):
        if self.executor:
            self.executor.shutdown(wait=False)
            self.executor = None
        self.cleanup_db_connections()
        self.queue.put(self.process_finished)

    def cleanup(self):
        logger.debug("Performing cleanup")
        if self.executor:
            self.executor.shutdown(wait=False)
            self.executor = None
        self.cleanup_db_connections()
        self.process_finished()

    def cleanup_db_connections(self):
        for db in list(self.active_db_connections):
            try:
                db.close()
            except Exception as e:
                logger.error(f"Error closing database connection: {e}")
            self.active_db_connections.discard(db)

    def destroy(self):
        logger.debug("Destroying RecipeListPage")
        self.cancel_event.set()
        if self.executor:
            self.executor.shutdown(wait=False)
        self.cleanup_db_connections()
        super().destroy()
