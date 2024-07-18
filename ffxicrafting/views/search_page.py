import threading
import tkinter as tk
import mysql.connector
from tkinter import ttk
from queue import Queue, Empty
from controllers import RecipeController, ItemController
from database import Database
from utils import TreeviewWithSort
from views import RecipeListPage


class SearchPage(RecipeListPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_open = True
        self.queue = Queue()
        self.create_search_page()
        self.check_queue()

    def create_search_page(self):
        self.parent.notebook.add(self, text="Search Recipes")

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var, font=("Helvetica", 14))
        self.search_entry.pack(pady=10)
        self.search_button = ttk.Button(self, text="Search", command=self.start_search_recipes)
        self.search_button.pack(pady=(0, 10))

        self.search_progress = ttk.Progressbar(self, mode='indeterminate', length=300)
        self.search_progress.pack(pady=10)
        self.search_progress.pack_forget()

        self.recipe_tree = TreeviewWithSort(self, columns=("nq", "hq", "levels", "ingredients"), show="headings")
        self.configure_recipe_treeview(self.recipe_tree)
        self.recipe_tree.pack(padx=10, pady=10, expand=True, fill="both")

        self.recipe_tree.bind("<Double-1>", self.show_recipe_details)
        self.recipe_tree.bind("<Button-1>", self.on_treeview_click)

    def configure_recipe_treeview(self, treeview):
        treeview.heading("nq", text="NQ")
        treeview.heading("hq", text="HQ")
        treeview.heading("levels", text="Craft Levels")
        treeview.heading("ingredients", text="Ingredients")
        treeview.column("levels", anchor=tk.CENTER)

    def start_search_recipes(self):
        self.search_button.config(text="Cancel", command=self.cancel_search)
        self.clear_treeview(self.recipe_tree)
        self.search_progress.pack_forget()
        self.search_progress.pack(pady=10, before=self.recipe_tree)
        self.search_progress.start()
        self.results = []
        self.total_results = 0
        self.is_open = True
        self.search_thread = threading.Thread(target=self.query_recipes, args=(self.search_var.get(),))
        self.search_thread.start()

    def cancel_search(self):
        self.is_open = False
        if hasattr(self, "search_thread") and self.search_thread.is_alive():
            self.search_thread.join(timeout=1)  # Timeout to avoid long blocking
        self.search_finished()

    def search_finished(self):
        self.search_progress.stop()
        self.search_progress.pack_forget()
        self.search_button.config(text="Search", command=self.start_search_recipes)
        self.search_button.config(state=tk.NORMAL)

    def query_recipes(self, search_term):
        try:
            for result in RecipeController.search_recipe_generator(search_term):
                if not self.is_open:
                    break
                self.process_single_result(result)
            self.queue.put(self.finalize_search)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.queue.put(self.search_finished)

    def process_single_result(self, recipe):
        nq_string = recipe.get_formatted_nq_result()
        hq_string = recipe.get_formatted_hq_results()
        levels_string = recipe.get_formatted_levels_string()
        ingredient_names_summarized = recipe.get_formatted_ingredient_names()

        for item in recipe.get_unique_ingredients():
            # None = the price has never been updated
            if (item.single_price is None or item.stack_price is None or
                    item.single_sell_freq is None or item.stack_sell_freq is None):
                ItemController.update_auction_data(item.item_id)

            # Always set vendor data in case merchant settings changed
            ItemController.update_vendor_data(item.item_id)

        for item in recipe.get_unique_results():
            # None = the price has never been updated
            if (item.single_price is None or item.stack_price is None or
                    item.single_sell_freq is None or item.stack_sell_freq is None):
                ItemController.update_auction_data(item.item_id)

        row = [nq_string, hq_string, levels_string, ingredient_names_summarized]
        self.results.append((recipe.id, row))
        self.queue.put(lambda: self.insert_single_into_treeview(recipe.id, row))

    def finalize_search(self):
        self.search_finished()

    def insert_single_into_treeview(self, recipe_id, row):
        self.recipe_tree.insert("", "end", iid=recipe_id, values=row)

    def check_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                task()
        except Empty:
            pass
        self.after(100, self.check_queue)

    def destroy(self):
        self.is_open = False
        if hasattr(self, "search_thread") and self.search_thread.is_alive():
            self.search_thread.join(timeout=1)  # Timeout to avoid long blocking
        # Close all active database connections asynchronously
        threading.Thread(target=Database().close_all_connections).start()
        super().destroy()
