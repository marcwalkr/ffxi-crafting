from functools import lru_cache
from tkinter import ttk
from .recipe_detail_page import RecipeDetailPage
from ..controllers import RecipeController


class RecipeListPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent.notebook)
        self.parent = parent

    @lru_cache(maxsize=None)
    def show_recipe_details(self, event):
        tree = event.widget
        if not tree.selection():
            return

        recipe_id = tree.selection()[0]

        recipe = RecipeController.get_recipe(recipe_id)
        detail_page = RecipeDetailPage(self.parent, recipe)
        self.parent.notebook.add(detail_page, text=f"Recipe {recipe.result_name} Details")
        self.parent.notebook.select(detail_page)

    def on_treeview_click(self, event):
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())

    def clear_treeview(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)
