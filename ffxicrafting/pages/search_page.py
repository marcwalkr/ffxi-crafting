import tkinter as tk
from tkinter import ttk
from utils.widgets import TreeviewWithSort
from functools import lru_cache
from controllers.recipe_controller import RecipeController
from pages.recipe_list_page import RecipeListPage


class SearchPage(RecipeListPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_search_page()

    def create_search_page(self):
        self.parent.notebook.add(self, text="Search Recipes")

        search_var = tk.StringVar()
        search_entry = ttk.Entry(self, textvariable=search_var, font=("Helvetica", 14))
        search_entry.pack(pady=10)
        search_button = ttk.Button(self, text="Search",
                                   command=lambda: self.search_recipes(search_var.get()))
        search_button.pack(pady=(0, 10))

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

    @lru_cache(maxsize=None)
    def search_recipes(self, search_term):
        self.clear_treeview(self.recipe_tree)
        results = RecipeController.search_recipe(search_term)

        for recipe in results:
            nq_string = recipe.get_formatted_nq_result()
            hq_string = recipe.get_formatted_hq_results()
            levels_string = recipe.get_formatted_levels_string()
            ingredient_names_summarized = recipe.get_formatted_ingredient_names()
            row = [nq_string, hq_string, levels_string, ingredient_names_summarized]
            self.recipe_tree.insert("", "end", iid=recipe.id, values=row)
