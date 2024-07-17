import tkinter as tk
from tkinter import ttk
from config.settings_manager import SettingsManager
from entities.crafter import Crafter
from utils.widgets import TreeviewWithSort


class RecipeDetailPage(ttk.Frame):
    def __init__(self, parent, recipe):
        self.previous_tab_index = parent.notebook.index("current")
        super().__init__(parent.notebook)
        self.parent = parent
        self.recipe = recipe
        self.create_detail_page()

    def create_detail_page(self):
        self.add_recipe_label(self.recipe.result_name)
        self.add_ingredients_tree()
        self.add_cost_per_synth_frame()
        self.add_results_tree()
        self.add_close_button()

    def add_recipe_label(self, text):
        recipe_label = ttk.Label(self, text=text)
        recipe_label.pack(pady=10)

    def add_ingredients_tree(self):
        ingredients_frame = ttk.Frame(self)
        ingredients_frame.pack(fill=tk.BOTH, expand=True)

        ingredient_columns = ("Ingredient", "Quantity", "Avg Single Price", "Avg Stack Price", "Vendor Price")
        self.ingredients_tree = TreeviewWithSort(ingredients_frame, columns=ingredient_columns, show="headings",
                                                 selectmode="browse")
        self.configure_treeview_columns(self.ingredients_tree, ingredient_columns)
        self.populate_ingredients_tree()
        self.ingredients_tree.pack(padx=10, pady=5, expand=True, fill="both")

        self.ingredients_tree.bind("<Button-1>", self.on_treeview_click)

    def add_cost_per_synth_frame(self):
        cost_per_synth_frame = ttk.Frame(self)
        cost_per_synth_frame.pack()

        cost_per_synth_label = ttk.Label(cost_per_synth_frame, text="Cost Per Synth:")
        cost_per_synth_label.pack(side=tk.LEFT)

        self.cost_per_synth_value_label = ttk.Label(cost_per_synth_frame)
        self.cost_per_synth_value_label.pack(side=tk.LEFT)

        self.update_cost_per_synth()

    def add_results_tree(self):
        results_frame = ttk.Frame(self)
        results_frame.pack(fill=tk.BOTH, expand=True)

        result_columns = ("Result", "Avg Single Price", "Avg Stack Price")
        self.results_tree = TreeviewWithSort(results_frame, columns=result_columns,
                                             show="headings", selectmode="browse")
        self.configure_treeview_columns(self.results_tree, result_columns)
        self.populate_results_tree()
        self.results_tree.pack(padx=10, pady=10, expand=True, fill="both")

        self.results_tree.bind("<Button-1>", self.on_treeview_click)

    def add_close_button(self):
        close_button = ttk.Button(self, text="Close", command=self.close_detail_page)
        close_button.pack(pady=(5, 10))

    def configure_treeview_columns(self, treeview, columns):
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor=tk.CENTER, stretch=True)

    def populate_ingredients_tree(self):
        ingredient_counts = self.recipe.get_ingredient_counts()

        for ingredient, quantity in ingredient_counts.items():
            single_price = ingredient.single_price if ingredient.single_price is not None else ""
            stack_price = ingredient.stack_price if ingredient.stack_price is not None else ""

            # Update vendor prices in case merchant settings changed
            ingredient.set_vendor_data()

            vendor_price = ingredient.min_vendor_price if ingredient.min_vendor_price is not None else ""
            ingredient_name = ingredient.get_formatted_name()
            self.ingredients_tree.insert("", "end", iid=ingredient.item_id, values=(
                ingredient_name, quantity, single_price, stack_price, vendor_price, self.recipe.id))

    def populate_results_tree(self):
        unique_results = self.recipe.get_unique_results()
        for result in unique_results:
            result_name = result.get_formatted_name()
            single_price = result.single_price if result.single_price is not None else ""
            stack_price = result.stack_price if result.stack_price is not None else ""
            self.results_tree.insert("", "end", iid=result.item_id, values=(result_name, single_price, stack_price,
                                                                            self.recipe.id))

    def update_cost_per_synth(self):
        skills = SettingsManager.get_skills()
        crafter = Crafter(*skills, self.recipe)

        crafter.synth.cost = crafter.synth.calculate_cost()

        value_text = f"{crafter.synth.cost} gil" if crafter.synth.cost is not None else "N/A"
        self.cost_per_synth_value_label.config(text=value_text)
        self.update()

    def close_detail_page(self):
        tab_id = self.parent.notebook.index(self)
        self.parent.notebook.forget(tab_id)
        self.parent.notebook.select(self.previous_tab_index)

    def on_treeview_click(self, event):
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())
