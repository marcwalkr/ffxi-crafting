import tkinter as tk
from tkinter import ttk
from entities import Crafter
from config import SettingsManager
from utils import TreeviewWithSort
from controllers import ItemController
from database import Database


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

        ingredient_columns = ("Ingredient", "Quantity", "AH Single Cost", "AH Stack Cost", "Vendor Cost")
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
        self.update_profits()

    def add_results_tree(self):
        results_frame = ttk.Frame(self)
        results_frame.pack(fill=tk.BOTH, expand=True)

        result_columns = ("Result", "Avg Single Price", "Avg Stack Price", "Single Profit", "Stack Profit")
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

        db = Database()  # Borrow a connection from the pool
        item_controller = ItemController(db)

        for ingredient, quantity in ingredient_counts.items():
            single_cost = int(ingredient.single_price * quantity) if ingredient.single_price else ""

            if ingredient.stack_price:
                single_cost_from_stack = ingredient.stack_price / ingredient.stack_size
                stack_cost = int(single_cost_from_stack * quantity)
            else:
                stack_cost = ""

            # Update vendor prices in case merchant settings changed
            item_controller.update_vendor_data(ingredient.item_id)

            vendor_cost = ingredient.min_vendor_price if ingredient.min_vendor_price is not None else ""
            ingredient_name = ingredient.get_formatted_name()
            self.ingredients_tree.insert("", "end", iid=ingredient.item_id, values=(
                ingredient_name, quantity, single_cost, stack_cost, vendor_cost, self.recipe.id))

        db.close()  # Return the connection to the pool

    def populate_results_tree(self):
        unique_results = self.recipe.get_unique_results()
        for result in unique_results:
            result_name = result.get_formatted_name()
            single_price = result.single_price if result.single_price is not None else ""
            stack_price = result.stack_price if result.stack_price is not None else ""
            single_profit = result.single_profit if result.single_profit is not None else ""
            stack_profit = result.stack_profit if result.stack_profit is not None else ""
            self.results_tree.insert("", "end", iid=result.item_id, values=(result_name, single_price, stack_price,
                                                                            single_profit, stack_profit, self.recipe.id))

    def update_cost_per_synth(self):
        skills = SettingsManager.get_skills()
        crafter = Crafter(*skills, self.recipe)

        crafter.synth.cost = crafter.synth.calculate_cost()

        value_text = f"{crafter.synth.cost} gil" if crafter.synth.cost is not None else "N/A"
        self.cost_per_synth_value_label.config(text=value_text)
        self.update()

    def update_profits(self):
        skills = SettingsManager.get_skills()
        crafter = Crafter(*skills, self.recipe)

        crafter.synth.cost = crafter.synth.calculate_cost()

        if crafter.synth.cost is not None:
            single_profits, stack_profits, _, _ = crafter.craft()

            for result in self.recipe.get_unique_results():
                result.single_profit = single_profits[result]
                result.stack_profit = stack_profits[result]

    def close_detail_page(self):
        tab_id = self.parent.notebook.index(self)
        self.parent.notebook.forget(tab_id)
        self.parent.notebook.select(self.previous_tab_index)

    def on_treeview_click(self, event):
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())
