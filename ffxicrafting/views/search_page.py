import tkinter as tk
from tkinter import ttk
from views import RecipeListPage


class SearchPage(RecipeListPage):
    def __init__(self, parent):
        self.action_button_text = "Search"
        super().__init__(parent)

    def get_tab_text(self):
        return "Search Recipes"

    def create_widgets(self):
        super().create_widgets()
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var, font=("Helvetica", 14))
        self.search_entry.pack(pady=10, before=self.action_button)
        self.search_entry.bind("<Return>", lambda event: self.start_process())

    def get_treeview_columns(self):
        return ("nq", "hq", "levels", "ingredients")

    def configure_treeview(self, treeview):
        treeview.heading("nq", text="NQ")
        treeview.heading("hq", text="HQ")
        treeview.heading("levels", text="Craft Levels")
        treeview.heading("ingredients", text="Ingredients")
        treeview.column("levels", anchor=tk.CENTER)

    def get_recipe_batch(self, batch_size, offset):
        return self.recipe_controller.search_recipe(self.search_var.get(), batch_size, offset)

    def format_row(self, craft_result):
        recipe = craft_result["crafter"].recipe

        return [
            recipe.get_formatted_nq_result(),
            recipe.get_formatted_hq_results(),
            recipe.get_formatted_levels_string(),
            recipe.get_formatted_ingredient_names()
        ]
