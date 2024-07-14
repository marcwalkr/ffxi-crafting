import tkinter as tk
from tkinter import ttk
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from controllers.vendor_controller import VendorController
from controllers.auction_controller import AuctionController
from config import Config
from crafter import Crafter
from synth import Synth
from utils import summarize_list, count_items, unique_preserve_order


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FFXI Crafting Tool")
        self.geometry("1280x800")

        self.configure_styles()
        self.create_main_frame()
        self.create_notebook()
        self.create_pages()

    def configure_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 14), padding=5)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10), padding=4)
        self.style.configure("Treeview", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both")

    def create_pages(self):
        self.create_search_page()
        self.create_profit_page()
        self.create_simulate_page()
        self.create_settings_page()

    def create_search_page(self):
        self.search_page = ttk.Frame(self.notebook)
        self.notebook.add(self.search_page, text="Search Recipes")

        search_var = tk.StringVar()
        search_entry = ttk.Entry(self.search_page, textvariable=search_var, font=("Helvetica", 14))
        search_entry.pack(pady=10)
        search_button = ttk.Button(self.search_page, text="Search",
                                   command=lambda: self.search_recipes(search_var.get()))
        search_button.pack(pady=(0, 10))

        self.recipe_tree = TreeviewWithSort(self.search_page, columns=("nq", "hq", "levels", "ingredients"),
                                            show="headings")
        self.configure_treeview(self.recipe_tree)
        self.recipe_tree.pack(padx=10, pady=10, expand=True, fill="both")

        self.recipe_tree.bind("<Double-1>", self.show_recipe_details)
        self.recipe_tree.bind("<Button-1>", self.on_treeview_click)

    def configure_treeview(self, treeview):
        treeview.heading("nq", text="NQ")
        treeview.heading("hq", text="HQ")
        treeview.heading("levels", text="Craft Levels")
        treeview.heading("ingredients", text="Ingredients")

    def create_profit_page(self):
        self.profit_page = ttk.Frame(self.notebook)
        self.notebook.add(self.profit_page, text="Profit Table")

        generate_button = ttk.Button(self.profit_page, text="Generate Table", command=self.generate_profit_table)
        generate_button.pack(pady=10)

        self.profit_tree = TreeviewWithSort(self.profit_page, columns=(
            "nq", "hq", "tier", "cost_per_synth", "profit_per_synth", "profit_per_storage"), show="headings")
        self.configure_profit_treeview(self.profit_tree)
        self.profit_tree.pack(padx=10, pady=10, expand=True, fill="both")

        self.profit_tree.bind("<Double-1>", self.show_recipe_details)
        self.profit_tree.bind("<Button-1>", self.on_treeview_click)

    def configure_profit_treeview(self, treeview):
        treeview.heading("nq", text="NQ")
        treeview.heading("hq", text="HQ")
        treeview.heading("tier", text="Tier")
        treeview.heading("cost_per_synth", text="Cost / Synth")
        treeview.heading("profit_per_synth", text="Profit / Synth")
        treeview.heading("profit_per_storage", text="Profit / Storage")

    def generate_profit_table(self):
        # Placeholder for generating the profit table
        # This function will be implemented later to populate the Treeview with recipe data
        pass

    def create_simulate_page(self):
        self.simulate_page = ttk.Frame(self.notebook)
        self.notebook.add(self.simulate_page, text="Simulate Synth")

    def create_settings_page(self):
        self.settings_page = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_page, text="Settings")

    def search_recipes(self, search_term):
        self.clear_treeview(self.recipe_tree)
        results = SynthController.search_recipe(search_term)

        for recipe in results:
            nq_string, hq_string, levels_string, ingredient_names_summarized = self.format_recipe_data(recipe)
            tree_values = [nq_string, hq_string, levels_string, ingredient_names_summarized]
            self.recipe_tree.insert("", "end", iid=recipe.id, values=tree_values)

    def clear_treeview(self, treeview):
        for i in treeview.get_children():
            treeview.delete(i)

    def format_recipe_data(self, recipe):
        nq_string = self.format_item_string(recipe.result, recipe.result_qty)
        hq_string = self.format_hq_string(recipe)
        levels_string = self.format_levels_string(recipe)
        ingredient_names_summarized = self.format_ingredient_names(recipe)
        return nq_string, hq_string, levels_string, ingredient_names_summarized

    def format_item_string(self, item_id, quantity):
        item_name = ItemController.get_formatted_item_name(item_id)
        return item_name if quantity == 1 else f"{item_name} x{quantity}"

    def format_hq_string(self, recipe):
        hq_strings = [
            self.format_item_string(recipe.result_hq1, recipe.result_hq1_qty),
            self.format_item_string(recipe.result_hq2, recipe.result_hq2_qty),
            self.format_item_string(recipe.result_hq3, recipe.result_hq3_qty)
        ]
        return ", ".join(unique_preserve_order(hq_strings))

    def format_levels_string(self, recipe):
        skills = {
            "Wood": recipe.wood,
            "Smith": recipe.smith,
            "Gold": recipe.gold,
            "Cloth": recipe.cloth,
            "Leather": recipe.leather,
            "Bone": recipe.bone,
            "Alchemy": recipe.alchemy,
            "Cook": recipe.cook
        }
        levels = [f"{skill} {level}" for skill, level in skills.items() if level > 0]
        return ", ".join(levels)

    def format_ingredient_names(self, recipe):
        ingredient_ids = [
            recipe.crystal, recipe.ingredient1, recipe.ingredient2, recipe.ingredient3,
            recipe.ingredient4, recipe.ingredient5, recipe.ingredient6, recipe.ingredient7,
            recipe.ingredient8
        ]
        ingredient_names = [ItemController.get_formatted_item_name(id) for id in ingredient_ids if id > 0]
        return summarize_list(ingredient_names)

    def show_recipe_details(self, event):
        if not self.recipe_tree.selection():
            return

        recipe_id = self.recipe_tree.selection()[0]
        recipe = SynthController.get_recipe(recipe_id)
        detail_page = self.create_detail_page(recipe)
        self.notebook.add(detail_page, text=f"Recipe {recipe.result_name} Details")
        self.notebook.select(detail_page)

    def create_detail_page(self, recipe):
        detail_page = ttk.Frame(self.notebook)
        self.add_recipe_label(detail_page, recipe.result_name)
        self.add_ingredients_tree(detail_page, recipe)
        self.add_cost_per_synth_frame(detail_page, recipe)
        self.add_results_tree(detail_page, recipe)
        self.add_close_button(detail_page)
        return detail_page

    def add_recipe_label(self, frame, text):
        recipe_label = ttk.Label(frame, text=text)
        recipe_label.pack(pady=10)

    def add_ingredients_tree(self, frame, recipe):
        ingredients_frame = ttk.Frame(frame)
        ingredients_frame.pack(fill=tk.BOTH, expand=True)

        ingredient_columns = ("Ingredient", "Quantity", "Single Price", "Stack Price", "Vendor Price")
        self.ingredients_tree = TreeviewWithSort(ingredients_frame, columns=ingredient_columns, show="headings",
                                                 selectmode="browse")
        self.configure_treeview_columns(self.ingredients_tree, ingredient_columns)
        self.populate_ingredients_tree(recipe)
        self.ingredients_tree.pack(padx=10, pady=5, expand=True, fill="both")

        self.ingredients_tree.bind("<Double-1>", self.edit_ingredient_price)
        self.ingredients_tree.bind("<Button-1>", self.on_treeview_click)

    def configure_treeview_columns(self, treeview, columns):
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor=tk.CENTER, stretch=True)

    def populate_ingredients_tree(self, recipe):
        ingredient_counts = count_items([i for i in self.get_ingredient_ids(recipe) if i > 0])
        for ingredient_id, quantity in ingredient_counts.items():
            ingredient_name = ItemController.get_formatted_item_name(ingredient_id)
            single_price, stack_price = self.get_auction_prices(ingredient_id)
            cheapest_vendor_price = self.get_cheapest_vendor_price(ingredient_id)
            self.ingredients_tree.insert("", "end", iid=ingredient_id, values=(
                ingredient_name, quantity, single_price, stack_price, cheapest_vendor_price, recipe.id))

    def get_ingredient_ids(self, recipe):
        return [
            recipe.crystal, recipe.ingredient1, recipe.ingredient2, recipe.ingredient3,
            recipe.ingredient4, recipe.ingredient5, recipe.ingredient6, recipe.ingredient7,
            recipe.ingredient8
        ]

    def get_auction_prices(self, item_id):
        auction_item = AuctionController.get_auction_item(item_id)
        if auction_item is None:
            return "", ""
        single_price = "" if auction_item.single_price == 0 else auction_item.single_price
        stack_price = "" if auction_item.stack_price == 0 else auction_item.stack_price
        return single_price, stack_price

    def get_cheapest_vendor_price(self, item_id):
        vendor_items = VendorController.get_vendor_items(item_id)
        if vendor_items:
            return min([vendor_item.price for vendor_item in vendor_items])
        return ""

    def add_cost_per_synth_frame(self, frame, recipe):
        cost_per_synth_frame = ttk.Frame(frame)
        cost_per_synth_frame.pack()

        cost_per_synth_label = ttk.Label(cost_per_synth_frame, text="Cost Per Synth:")
        cost_per_synth_label.pack(side=tk.LEFT)

        self.cost_per_synth_value_label = ttk.Label(cost_per_synth_frame)
        self.cost_per_synth_value_label.pack(side=tk.LEFT)

        self.update_cost_per_synth(recipe)

    def add_results_tree(self, frame, recipe):
        results_frame = ttk.Frame(frame)
        results_frame.pack(fill=tk.BOTH, expand=True)

        result_columns = ("Result", "Single Price", "Stack Price")
        self.results_tree = TreeviewWithSort(results_frame, columns=result_columns,
                                             show="headings", selectmode="browse")
        self.configure_treeview_columns(self.results_tree, result_columns)
        self.populate_results_tree(recipe)
        self.results_tree.pack(padx=10, pady=10, expand=True, fill="both")

        self.results_tree.bind("<Double-1>", self.edit_result_price)
        self.results_tree.bind("<Button-1>", self.on_treeview_click)

    def populate_results_tree(self, recipe):
        unique_result_ids = unique_preserve_order(
            [recipe.result, recipe.result_hq1, recipe.result_hq2, recipe.result_hq3])
        for result_id in unique_result_ids:
            result_name = ItemController.get_formatted_item_name(result_id)
            single_price, stack_price = self.get_auction_prices(result_id)
            self.results_tree.insert("", "end", iid=result_id, values=(
                result_name, single_price, stack_price, recipe.id))

    def add_close_button(self, frame):
        close_button = ttk.Button(frame, text="Close", command=lambda: self.close_detail_page(frame))
        close_button.pack(pady=(5, 10))

    def edit_and_save_prices(self, tree, item_id, price_indices, popup_title, recipe_id):
        item_values = tree.item(item_id, "values")
        popup = self.create_popup(popup_title, item_values[0])

        single_price_entry = self.create_price_entry(popup, "Single Price:", item_values[price_indices[0]], 2)
        stack_price_entry = self.create_price_entry(popup, "Stack Price:", item_values[price_indices[1]], 3)

        save_button = ttk.Button(popup, text="Save", command=lambda: self.save_prices(
            popup, item_id, single_price_entry, stack_price_entry, tree, price_indices, recipe_id))
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
        recipe_id = self.ingredients_tree.item(item_id, "values")[5]
        self.edit_and_save_prices(self.ingredients_tree, item_id, [2, 3], "Edit Ingredient Prices", recipe_id)

    def edit_result_price(self, event):
        if not self.results_tree.selection():
            return

        item_id = self.results_tree.selection()[0]
        recipe_id = self.results_tree.item(item_id, "values")[3]
        self.edit_and_save_prices(self.results_tree, item_id, [1, 2], "Edit Result Prices", recipe_id)

    def save_prices(self, popup, item_id, single_price_entry, stack_price_entry, tree, price_indices, recipe_id):
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

        recipe = SynthController.get_recipe(recipe_id)
        self.update_cost_per_synth(recipe)
        popup.destroy()

    def update_cost_per_synth(self, recipe):
        skill_set = Config.get_skill_set()
        crafter = Crafter(skill_set)
        synth = Synth(recipe, crafter)
        cost_per_synth = synth.calculate_cost()

        value_text = f"{cost_per_synth:.2f} gil" if cost_per_synth is not None else "N/A"
        self.cost_per_synth_value_label.config(text=value_text)
        self.update()

    def close_detail_page(self, detail_page):
        tab_id = self.notebook.index(detail_page)
        self.notebook.forget(tab_id)

    def on_treeview_click(self, event):
        tree = event.widget
        region = tree.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            tree.selection_remove(tree.selection())


class TreeviewWithSort(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._init_sorting()

    def _init_sorting(self):
        for col in self["columns"]:
            self.heading(col, text=col, command=lambda c=col: self._sort_by(c, False))

    def _sort_by(self, col, descending):
        data = [(self.set(child, col), child) for child in self.get_children('')]
        data.sort(reverse=descending)

        for idx, (val, child) in enumerate(data):
            self.move(child, "", idx)

        self.heading(col, command=lambda: self._sort_by(col, not descending))


if __name__ == "__main__":
    app = App()
    app.mainloop()
