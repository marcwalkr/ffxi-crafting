import threading
import concurrent.futures
import traceback
from tkinter import ttk
from queue import Queue, Empty
from concurrent.futures import ThreadPoolExecutor
from views import RecipeDetailPage
from controllers import RecipeController
from database import Database


class RecipeListPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent.notebook)
        self.parent = parent
        self.is_open = True
        self.queue = Queue()
        self.init_executor()
        self.active_db_connections = []
        self.create_widgets()
        self.check_queue()

    def create_widgets(self):
        pass

    def init_executor(self):
        self.executor = ThreadPoolExecutor(max_workers=15)
        self.futures = []
        self.query_recipes_future = None

    def cleanup_db_connections(self):
        while self.active_db_connections:
            db = self.active_db_connections.pop()
            try:
                db.close()
            except Exception as e:
                print(f"Error closing database connection: {e}")

    def check_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                task()
        except Empty:
            pass
        self.after(100, self.check_queue)

    def show_recipe_details(self, event):
        tree = event.widget
        if not tree.selection():
            return

        recipe_id = tree.selection()[0]
        values = tree.item(recipe_id, "values")
        synth_cost = values[-1]

        db = Database()
        recipe_controller = RecipeController(db)

        recipe = recipe_controller.get_recipe(int(recipe_id))
        detail_page = RecipeDetailPage(self.parent, recipe, synth_cost)
        self.parent.notebook.add(detail_page, text=f"Recipe {recipe.result_name} Details")
        self.parent.notebook.select(detail_page)

        db.close()

    def on_treeview_click(self, event):
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())

    def clear_treeview(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

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
                traceback.print_exc()
        self.cleanup_db_connections()
        self.process_finished()

    def process_finished(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.action_button.config(text=self.action_button_text, command=self.start_process, state="normal")

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
                    traceback.print_exc()
                    self.queue.put(self.process_finished)
                    return
            self.queue.put(self.finalize_process)

    def query_recipes(self):
        pass

    def process_batch(self, results):
        pass

    def insert_single_into_treeview(self, recipe_id, row):
        self.treeview.insert("", "end", iid=recipe_id, values=row)

    def finalize_process(self):
        pass

    def destroy(self):
        self.is_open = False
        self.executor.shutdown(wait=False)
        self.cleanup_db_connections()
        super().destroy()
