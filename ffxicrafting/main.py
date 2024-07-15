import re
import tkinter as tk
from tkinter import ttk
from controllers.recipe_controller import RecipeController
from controllers.auction_controller import AuctionController
from entities.crafter import Crafter
from config.settings_manager import SettingsManager


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FFXI Crafting Tool")
        self.geometry("1280x800")

        self.settings = SettingsManager.load_settings()
        self.configure_styles()
        self.create_main_frame()
        self.create_notebook()
        self.create_pages()

    def save_settings(self):
        settings = {
            "profit_table": self.get_number_settings(self.profit_table_settings),
            "synth": self.get_number_settings(self.synth_settings),
            "skill_levels": self.get_vertical_number_settings(self.skill_levels_settings),
            "merchants": self.get_boolean_settings(self.merchants_settings)
        }
        SettingsManager.save_settings(settings)

    def get_number_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                settings[label] = child.get()
            elif isinstance(child, ttk.Frame):
                settings.update(self.get_number_settings(child))  # Recursively check nested frames
        return settings

    def get_vertical_number_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                settings[label] = child.get()
            elif isinstance(child, ttk.Frame):
                settings.update(self.get_vertical_number_settings(child))  # Recursively check nested frames
        return settings

    def get_boolean_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Checkbutton):
                label = child.cget("text").lower().replace(" ", "_")
                settings[label] = child.instate(['selected'])
            elif isinstance(child, ttk.Frame):
                settings.update(self.get_boolean_settings(child))  # Recursively check nested frames
        return settings

    def configure_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 14), padding=5)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10), padding=4)
        self.style.configure("Treeview", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("Custom.TCheckbutton", font=("Helvetica", 14))

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
        self.configure_recipe_treeview(self.recipe_tree)
        self.recipe_tree.pack(padx=10, pady=10, expand=True, fill="both")

        self.recipe_tree.bind("<Double-1>", self.show_recipe_details)
        self.recipe_tree.bind("<Button-1>", self.on_treeview_click)

    def configure_recipe_treeview(self, treeview):
        treeview.heading("nq", text="NQ")
        treeview.heading("hq", text="HQ")
        treeview.heading("levels", text="Craft Levels")
        treeview.heading("ingredients", text="Ingredients")

        # Center craft levels
        treeview.column("levels", anchor=tk.CENTER)

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

        # Center columns
        treeview.column("tier", anchor=tk.CENTER)
        treeview.column("cost_per_synth", anchor=tk.CENTER)
        treeview.column("profit_per_synth", anchor=tk.CENTER)
        treeview.column("profit_per_storage", anchor=tk.CENTER)

    def generate_profit_table(self):
        self.clear_treeview(self.profit_tree)

        skills = SettingsManager.get_skills()
        skill_look_ahead = SettingsManager.get_skill_look_ahead()
        recipes = RecipeController.get_recipes_by_craft_levels(*(skill - skill_look_ahead for skill in skills))
        synth_profit_threshold = SettingsManager.get_profit_per_synth()
        storage_profit_threshold = SettingsManager.get_profit_per_storage()
        simulation_trials = SettingsManager.get_simulation_trials()

        for recipe in recipes:
            crafter = Crafter(*skills, recipe)

            crafter.synth.cost = crafter.synth.calculate_cost()
            if crafter.synth.cost is None:
                continue

            profit_per_synth, profit_per_storage = crafter.craft(simulation_trials)
            if profit_per_synth < synth_profit_threshold or profit_per_storage < storage_profit_threshold:
                continue

            nq_string = recipe.get_formatted_nq_result()
            hq_string = recipe.get_formatted_hq_results()
            row = [nq_string, hq_string, crafter.synth.tier,
                   crafter.synth.cost, profit_per_synth, profit_per_storage]
            self.profit_tree.insert("", "end", iid=recipe.id, values=row)

    def create_simulate_page(self):
        self.simulate_page = ttk.Frame(self.notebook)
        self.notebook.add(self.simulate_page, text="Simulate Synth")

    def create_settings_page(self):
        self.settings_page = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_page, text="Settings")

        self.create_settings_categories()

    def create_settings_categories(self):
        categories = [
            ("Profit Table", self.create_profit_table_settings),
            ("Synth", self.create_synth_settings),
            ("Skill Levels and Merchants", self.create_skill_levels_and_merchants_settings)
        ]

        for category_name, create_method in categories:
            frame = ttk.LabelFrame(self.settings_page, text=category_name)
            frame.pack(fill="x", padx=10, pady=5)
            create_method(frame)

        save_button = ttk.Button(self.settings_page, text="Save", command=self.save_settings)
        save_button.pack(pady=10)

    def create_profit_table_settings(self, frame):
        self.profit_table_settings = frame
        settings = [
            ("Profit / Synth", 0),
            ("Profit / Storage", 0),
            ("Min Sell Price", 0)
        ]
        self.create_number_settings(frame, settings, self.settings.get("profit_table", {}))

    def create_synth_settings(self, frame):
        self.synth_settings = frame
        settings = [
            ("Skill Look Ahead", 0),
            ("Simulation Trials", 1000)
        ]
        self.create_number_settings(frame, settings, self.settings.get("synth", {}))

    def create_skill_levels_and_merchants_settings(self, frame):
        skill_levels_frame = ttk.Frame(frame)
        skill_levels_frame.pack(side="left", fill="y", padx=5, pady=5)
        self.skill_levels_settings = skill_levels_frame
        self.create_vertical_number_settings(skill_levels_frame, [
            ("Wood", 0),
            ("Smith", 0),
            ("Gold", 0),
            ("Cloth", 0),
            ("Leather", 0),
            ("Bone", 0),
            ("Alchemy", 0),
            ("Cook", 0)
        ], self.settings.get("skill_levels", {}))

        merchants_frame = ttk.Frame(frame)
        merchants_frame.pack(side="left", fill="y", padx=5, pady=5)
        self.merchants_settings = merchants_frame
        self.create_two_column_boolean_settings(merchants_frame, [
            "Guilds", "Aragoneu", "Derfland", "Elshimo Lowlands", "Elshimo Uplands", "Fauregandi",
            "Gustaberg", "Kolshushu", "Kuzotz", "Li'Telor", "Movalpolos", "Norvallen", "Qufim",
            "Ronfaure", "Sarutabaruta", "Tavnazian Archipelago", "Valdeaunia", "Vollbow", "Zulkheim"
        ], self.settings.get("merchants", {}))

    def create_number_settings(self, frame, settings, saved_settings):
        for setting, default in settings:
            label = ttk.Label(frame, text=setting)
            label.pack(side="left", padx=5, pady=5)
            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(frame, width=10, name=entry_name)
            entry.insert(0, saved_settings.get(entry_name, default))
            entry.pack(side="left", padx=5, pady=5)

    def create_vertical_number_settings(self, frame, settings, saved_settings):
        for setting, default in settings:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            label = ttk.Label(row_frame, text=setting)
            label.pack(side="left", padx=5, pady=5)
            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(row_frame, width=10, name=entry_name)
            entry.insert(0, saved_settings.get(entry_name, default))
            entry.pack(side="right", padx=5, pady=5)

    def create_two_column_boolean_settings(self, frame, settings, saved_settings):
        left_frame = ttk.Frame(frame)
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        right_frame = ttk.Frame(frame)
        right_frame.pack(side="left", fill="y", padx=5, pady=5)

        for i, setting in enumerate(settings):
            target_frame = left_frame if i % 2 == 0 else right_frame
            var = tk.BooleanVar(value=saved_settings.get(setting.lower().replace(" ", "_"), False))
            checkbutton = ttk.Checkbutton(target_frame, text=setting, variable=var, style="Custom.TCheckbutton")
            checkbutton.pack(anchor="w", padx=5, pady=2)
            checkbutton.var = var

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

    def clear_treeview(self, treeview):
        for i in treeview.get_children():
            treeview.delete(i)

    def show_recipe_details(self, event):
        tree = event.widget
        if not tree.selection():
            return

        recipe_id = tree.selection()[0]
        recipe = RecipeController.get_recipe(recipe_id)
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
        ingredient_counts = recipe.get_ingredient_counts()

        for ingredient, quantity in ingredient_counts.items():
            single_price = ingredient.single_price if ingredient.single_price is not None else ""
            stack_price = ingredient.stack_price if ingredient.stack_price is not None else ""
            vendor_price = ingredient.min_vendor_price if ingredient.min_vendor_price is not None else ""
            ingredient_name = ingredient.get_formatted_name()
            self.ingredients_tree.insert("", "end", iid=ingredient.item_id, values=(
                ingredient_name, quantity, single_price, stack_price, vendor_price, recipe.id))

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
        unique_results = recipe.get_unique_results()
        for result in unique_results:
            result_name = result.get_formatted_name()
            single_price, stack_price = result.get_auction_prices()
            single_price = "" if single_price is None else single_price
            stack_price = "" if stack_price is None else stack_price
            self.results_tree.insert("", "end", iid=result.item_id, values=(result_name, single_price, stack_price,
                                                                            recipe.id))

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

        recipe = RecipeController.get_recipe(recipe_id)
        self.update_cost_per_synth(recipe)
        popup.destroy()

    def update_cost_per_synth(self, recipe):
        skills = SettingsManager.get_skills()
        crafter = Crafter(*skills, recipe)

        crafter.synth.cost = crafter.synth.calculate_cost()

        value_text = f"{crafter.synth.cost:.2f} gil" if crafter.synth.cost is not None else "N/A"
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
        def convert(value):
            if value == "":
                return float('-inf') if descending else float('inf')
            try:
                return float(value)
            except ValueError:
                return value

        def natural_keys(text):
            return [convert(c) if c.isdigit() else c for c in re.split(r'(\d+)', text)]

        data = [(natural_keys(self.set(child, col)), child) for child in self.get_children('')]
        data.sort(reverse=descending)

        for idx, (val, child) in enumerate(data):
            self.move(child, "", idx)

        self.heading(col, command=lambda: self._sort_by(col, not descending))


if __name__ == "__main__":
    app = App()
    app.mainloop()
