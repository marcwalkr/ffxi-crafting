import tkinter as tk
from tkinter import ttk
import threading
from utils.widgets import TreeviewWithSort
from controllers.recipe_controller import RecipeController
from pages.recipe_list_page import RecipeListPage


class SearchPage(RecipeListPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_search_page()

    def create_search_page(self):
        self.parent.notebook.add(self, text="Search Recipes")

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var, font=("Helvetica", 14))
        self.search_entry.pack(pady=10)
        self.search_button = ttk.Button(self, text="Search",
                                        command=self.start_search_recipes)
        self.search_button.pack(pady=(0, 10))

        self.search_progress = ttk.Progressbar(self, mode='indeterminate', length=300)
        self.search_progress.pack(pady=10)
        self.search_progress.pack_forget()

        self.recipe_tree = TreeviewWithSort(self, columns=("nq", "hq", "levels", "ingredients"),
                                            show="headings")
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
        self.search_button.config(state=tk.DISABLED)
        self.clear_treeview(self.recipe_tree)
        self.search_progress.pack_forget()
        self.search_progress.pack(pady=10, before=self.recipe_tree)
        self.search_progress.start()
        threading.Thread(target=self.query_recipes, args=(self.search_var.get(),)).start()

    def query_recipes(self, search_term):
        results = RecipeController.search_recipe(search_term)
        self.total_results = len(results)
        self.results = results
        self.after(10, self.update_search_progress, 0, [])

    def update_search_progress(self, index, batch):
        if index < self.total_results:
            recipe = self.results[index]
            nq_string = recipe.get_formatted_nq_result()
            hq_string = recipe.get_formatted_hq_results()
            levels_string = recipe.get_formatted_levels_string()
            ingredient_names_summarized = recipe.get_formatted_ingredient_names()
            row = [nq_string, hq_string, levels_string, ingredient_names_summarized]
            batch.append((recipe.id, row))

            if len(batch) >= 10:
                for item in batch:
                    self.recipe_tree.insert("", "end", iid=item[0], values=item[1])
                batch.clear()

            self.after(10, self.update_search_progress, index + 1, batch)
        else:
            for item in batch:
                self.recipe_tree.insert("", "end", iid=item[0], values=item[1])
            self.search_progress.stop()
            self.search_progress.pack_forget()
            self.search_button.config(state=tk.NORMAL)
