import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from tkinter import ttk
from queue import Queue, Empty
from abc import ABC
from utils import TreeviewWithSort
from views import RecipeDetailPage
from database import Database
from controllers import RecipeController, CraftingController, ItemController


class RecipeListPage(ttk.Frame, ABC):
    def __init__(self, parent):
        super().__init__(parent.notebook)
        self.parent = parent
        self.recipe_controller = RecipeController()
        self.is_open = True
        self.queue = Queue()
        self.init_executor()
        self.active_db_connections = []
        self.create_widgets()
        self.check_queue()

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

    def query_recipes(self):
        try:
            batch_size = 25
            offset = 0
            search_finished = False

            while self.is_open and not search_finished:
                results = self.get_recipe_batch(batch_size, offset)

                if len(results) < batch_size:
                    search_finished = True

                self.futures.append(self.executor.submit(self.process_batch, results))

                offset += batch_size

        except Exception as e:
            print(f"Error: {e}")
            self.queue.put(self.process_finished)

    def get_recipe_batch(self, batch_size, offset):
        raise NotImplementedError("Subclasses must implement get_recipe_batch()")

    def process_single_recipe(self, recipe, crafting_controller):
        if not self.is_open:
            return

        craft_result = crafting_controller.simulate_craft(recipe)

        if not craft_result:
            return

        if self.should_display_recipe(craft_result):
            row = self.format_row(craft_result)
            self.queue.put(lambda: self.insert_single_into_treeview(recipe.id, row))

    def should_display_recipe(self, craft_result):
        return True

    def format_row(self, craft_result):
        raise NotImplementedError("Subclasses must implement format_row()")

    def finalize_process(self):
        self.process_finished()

    def init_executor(self):
        self.executor = ThreadPoolExecutor(max_workers=15)
        self.futures = []
        self.query_recipes_future = None

    def check_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                task()
        except Empty:
            pass
        self.after(100, self.check_queue)

    def start_process(self):
        self.init_executor()
        self.action_button.config(text="Cancel", command=self.cancel_process)
        self.clear_treeview(self.treeview)
        self.progress_bar.pack_forget()
        self.progress_bar.pack(pady=10, before=self.treeview)
        self.progress_bar.start()
        self.is_open = True

        self.query_recipes_future = self.executor.submit(self.query_recipes)
        self.check_futures()

    def cancel_process(self):
        self.is_open = False
        self.action_button.config(text="Canceling...", state="disabled")
        self.executor.shutdown(wait=False)
        threading.Thread(target=self.wait_for_cancellation).start()

    def wait_for_cancellation(self):
        for future in self.futures:
            future.cancel()
        for future in self.futures:
            try:
                future.result()
            except concurrent.futures.CancelledError:
                pass
            except Exception as e:
                print(f"Error during cancellation: {e}")
        self.cleanup_db_connections()
        self.process_finished()

    def process_finished(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.action_button.config(text=self.action_button_text, command=self.start_process, state="normal")

    def process_batch(self, recipes):
        db = Database()
        self.active_db_connections.append(db)

        item_controller = ItemController(db)
        crafting_controller = CraftingController(item_controller)

        try:
            for recipe in recipes:
                if not self.is_open:
                    break
                self.process_single_recipe(recipe, crafting_controller)
        finally:
            db.close()
            self.active_db_connections.remove(db)

    def check_futures(self):
        incomplete_futures = [f for f in self.futures if not f.done()]
        if incomplete_futures or (self.query_recipes_future and not self.query_recipes_future.done()):
            self.after(100, self.check_futures)
        else:
            for future in self.futures:
                try:
                    future.result()
                except concurrent.futures.CancelledError:
                    pass
                except Exception as e:
                    print(f"Error in future: {e}")
                    self.queue.put(self.process_finished)
                    return
            self.queue.put(self.finalize_process)

    def insert_single_into_treeview(self, recipe_id, row):
        self.treeview.insert("", "end", iid=recipe_id, values=row)

    def on_treeview_click(self, event):
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())

    def clear_treeview(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

    def show_recipe_details(self, event):
        tree = event.widget
        if not tree.selection():
            return

        recipe_id = tree.selection()[0]

        recipe = self.recipe_controller.get_recipe(int(recipe_id))
        detail_page = RecipeDetailPage(self.parent, recipe)
        self.parent.notebook.add(detail_page, text=f"Recipe {recipe.result_name} Details")
        self.parent.notebook.select(detail_page)

    def cleanup_db_connections(self):
        while self.active_db_connections:
            db = self.active_db_connections.pop()
            try:
                db.close()
            except Exception as e:
                print(f"Error closing database connection: {e}")

    def destroy(self):
        self.is_open = False
        self.executor.shutdown(wait=False)
        self.cleanup_db_connections()
        super().destroy()
