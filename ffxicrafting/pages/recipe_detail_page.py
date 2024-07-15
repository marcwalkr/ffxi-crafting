import tkinter as tk
from tkinter import ttk
from utils.widgets import TreeviewWithSort
from controllers.auction_controller import AuctionController
from config.settings_manager import SettingsManager
from entities.crafter import Crafter


class RecipeDetailPage(ttk.Frame):
    def __init__(self, parent, recipe):
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

        ingredient_columns = ("Ingredient", "Quantity", "Single Price", "Stack Price", "Vendor Price")
        self.ingredients_tree = TreeviewWithSort(ingredients_frame, columns=ingredient_columns, show="headings",
                                                 selectmode="browse")
        self.configure_treeview_columns(self.ingredients_tree, ingredient_columns)
        self.populate_ingredients_tree()
        self.ingredients_tree.pack(padx=10, pady=5, expand=True, fill="both")

        self.ingredients_tree.bind("<Double-1>", self.edit_ingredient_price)
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

        result_columns = ("Result", "Single Price", "Stack Price")
        self.results_tree = TreeviewWithSort(results_frame, columns=result_columns,
                                             show="headings", selectmode="browse")
        self.configure_treeview_columns(self.results_tree, result_columns)
        self.populate_results_tree()
        self.results_tree.pack(padx=10, pady=10, expand=True, fill="both")

        self.results_tree.bind("<Double-1>", self.edit_result_price)
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
            vendor_price = ingredient.min_vendor_price if ingredient.min_vendor_price is not None else ""
            ingredient_name = ingredient.get_formatted_name()
            self.ingredients_tree.insert("", "end", iid=ingredient.item_id, values=(
                ingredient_name, quantity, single_price, stack_price, vendor_price, self.recipe.id))

    def populate_results_tree(self):
        unique_results = self.recipe.get_unique_results()
        for result in unique_results:
            result_name = result.get_formatted_name()
            single_price, stack_price = result.get_auction_prices()
            single_price = "" if single_price is None else single_price
            stack_price = "" if stack_price is None else stack_price
            self.results_tree.insert("", "end", iid=result.item_id, values=(result_name, single_price, stack_price,
                                                                            self.recipe.id))

    def edit_and_save_prices(self, tree, item_id, price_indices, popup_title):
        item_values = tree.item(item_id, "values")
        popup = self.create_popup(popup_title, item_values[0])

        single_price_entry = self.create_price_entry(popup, "Single Price:", item_values[price_indices[0]], 2)
        stack_price_entry = self.create_price_entry(popup, "Stack Price:", item_values[price_indices[1]], 3)

        save_button = ttk.Button(popup, text="Save", command=lambda: self.save_prices(
            popup, item_id, single_price_entry, stack_price_entry, tree, price_indices))
        save_button.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew", padx=20)

        self.center_popup(popup)

    def create_popup(self, title, item_name):
        popup = tk.Toplevel(self)
        popup.title(title)
        ttk.Label(popup, text=item_name).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        return popup

    def create_price_entry(self, popup, label_text, initial_value, row):
        ttk.Label(popup, text=label_text).grid(row=row, column=0, padx=10, pady=5, sticky='e')
        price_entry = ttk.Entry(popup, width=15)
        price_entry.insert(0, initial_value)
        price_entry.grid(row=row, column=1, padx=10, pady=5)
        return price_entry

    def center_popup(self, popup):
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        popup_width = 300
        popup_height = 240

        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2

        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        popup.grid_columnconfigure(0, weight=1)
        popup.grid_columnconfigure(1, weight=1)

    def edit_ingredient_price(self, event):
        if not self.ingredients_tree.selection():
            return

        item_id = self.ingredients_tree.selection()[0]
        self.edit_and_save_prices(self.ingredients_tree, item_id, [2, 3], "Edit Ingredient Prices")

    def edit_result_price(self, event):
        if not self.results_tree.selection():
            return

        item_id = self.results_tree.selection()[0]
        self.edit_and_save_prices(self.results_tree, item_id, [1, 2], "Edit Result Prices")

    def save_prices(self, popup, item_id, single_price_entry, stack_price_entry, tree, price_indices):
        single_price = single_price_entry.get()
        stack_price = stack_price_entry.get()

        values = list(tree.item(item_id, "values"))
        values[price_indices[0]] = single_price
        values[price_indices[1]] = stack_price
        tree.item(item_id, values=values)

        single_price = 0 if single_price == "" else single_price
        stack_price = 0 if stack_price == "" else stack_price

        if AuctionController.auction_item_exists(item_id):
            AuctionController.update_auction_item(item_id, single_price, stack_price)
        else:
            AuctionController.add_auction_item(item_id, single_price, stack_price)

        self.update_cost_per_synth()
        popup.destroy()

    def update_cost_per_synth(self):
        skills = SettingsManager.get_skills()
        crafter = Crafter(*skills, self.recipe)

        crafter.synth.cost = crafter.synth.calculate_cost()

        value_text = f"{crafter.synth.cost:.2f} gil" if crafter.synth.cost is not None else "N/A"
        self.cost_per_synth_value_label.config(text=value_text)
        self.update()

    def close_detail_page(self):
        tab_id = self.parent.notebook.index(self)
        self.parent.notebook.forget(tab_id)

    def on_treeview_click(self, event):
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())
