import tkinter as tk
from tkinter import ttk
from utils import TreeviewWithSort


class RecipeDetailPage(ttk.Frame):
    def __init__(self, parent, recipe, synth_cost):
        self.previous_tab_index = parent.notebook.index("current")
        super().__init__(parent.notebook)
        self.parent = parent
        self.recipe = recipe
        self.synth_cost = synth_cost
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

        ingredient_columns = ("Ingredient", "Quantity", "AH Single Cost", "AH Stack Cost", "Vendor Cost", "Guild Cost")
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

        value_text = f"{self.synth_cost} gil" if self.synth_cost != "None" else "N/A"
        self.cost_per_synth_value_label.config(text=value_text)

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

        for ingredient, quantity in ingredient_counts.items():
            ingredient_name = ingredient.get_formatted_name()

            single_cost = int(ingredient.single_price * quantity) if ingredient.single_price else ""

            if ingredient.stack_price:
                single_cost_from_stack = ingredient.stack_price / ingredient.stack_size
                stack_cost = int(single_cost_from_stack * quantity)
                stack_cost_string = f"{int(ingredient.stack_price)} ({stack_cost})"
            else:
                stack_cost_string = ""

            vendor_cost = ingredient.vendor_cost if ingredient.vendor_cost is not None else ""
            guild_cost = ingredient.guild_cost if ingredient.guild_cost is not None else ""

            self.ingredients_tree.insert("", "end", iid=ingredient.item_id, values=(
                ingredient_name, quantity, single_cost, stack_cost_string, vendor_cost, guild_cost, self.recipe.id))

    def populate_results_tree(self):
        unique_results = self.recipe.get_unique_results()
        for result in unique_results:
            result_name = result.get_formatted_name()
            single_price = result.single_price if result.single_price is not None else ""
            stack_price = result.stack_price if result.stack_price is not None else ""
            single_profit = int(result.single_profit) if result.single_profit is not None else ""
            stack_profit = int(result.stack_profit) if result.stack_profit is not None else ""
            self.results_tree.insert("", "end", iid=result.item_id, values=(result_name, single_price, stack_price,
                                                                            single_profit, stack_profit, self.recipe.id))

    def close_detail_page(self):
        tab_id = self.parent.notebook.index(self)
        self.parent.notebook.forget(tab_id)
        self.parent.notebook.select(self.previous_tab_index)

    def on_treeview_click(self, event):
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())
