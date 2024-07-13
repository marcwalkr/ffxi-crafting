import tkinter as tk
from tkinter import ttk
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from controllers.vendor_controller import VendorController
from controllers.auction_controller import AuctionController
from config import Config
from crafter import Crafter
from synth import Synth
from helpers import summarize_list, count_items


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FFXI Crafting Tool")
        self.geometry("800x700")

        # Configure styles
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 14), padding=5)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10), padding=4)
        self.style.configure("Treeview", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))

        # Create the main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

        # Create the notebook
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both")

        # Create different pages
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

        self.recipe_tree = ttk.Treeview(self.search_page, columns=("item", "levels", "ingredients"), show="headings")
        self.recipe_tree.heading("item", text="Item")
        self.recipe_tree.heading("levels", text="Craft Levels")
        self.recipe_tree.heading("ingredients", text="Ingredients")
        self.recipe_tree.pack(padx=10, pady=10, expand=True, fill="both")
        self.recipe_tree.bind("<Double-1>", self.show_recipe_details)

    def create_profit_page(self):
        self.profit_page = ttk.Frame(self.notebook)
        self.notebook.add(self.profit_page, text="Profit Table")

    def create_simulate_page(self):
        self.simulate_page = ttk.Frame(self.notebook)
        self.notebook.add(self.simulate_page, text="Simulate Synth")

    def create_settings_page(self):
        self.settings_page = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_page, text="Settings")

    def search_recipes(self, search_term):
        # Clear the treeview and perform the search
        for i in self.recipe_tree.get_children():
            self.recipe_tree.delete(i)

        results = SynthController.search_recipe(search_term)

        for result in results:
            # Create a string representing the required crafting levels
            skills = {
                "Wood": result.wood,
                "Smith": result.smith,
                "Gold": result.gold,
                "Cloth": result.cloth,
                "Leather": result.leather,
                "Bone": result.bone,
                "Alchemy": result.alchemy,
                "Cook": result.cook
            }

            levels = [f"{skill} {level}" for skill, level in skills.items() if level > 0]
            levels_string = ", ".join(levels)

            ingredient_ids = [result.crystal, result.ingredient1, result.ingredient2, result.ingredient3,
                              result.ingredient4, result.ingredient5, result.ingredient6, result.ingredient7,
                              result.ingredient8]

            # Get ingredient names from non-zero ingredient ids
            ingredient_names = [ItemController.get_item(id).sort_name.replace("_", " ").title()
                                for id in ingredient_ids if id > 0]

            # Summarize ingredients in a string e.g. [apple, orange, orange] -> "apple, orange x2"
            ingredient_names_summarized = summarize_list(ingredient_names)

            tree_values = [result.result_name, levels_string, ingredient_names_summarized]

            # Set the iid to the recipe id to retrieve in the detail page
            self.recipe_tree.insert("", "end", iid=result.id, values=tree_values)

    def show_recipe_details(self, event):
        # The tree iid was set to the recipe id
        recipe_id = self.recipe_tree.selection()[0]

        # Get the recipe object
        recipe = SynthController.get_recipe(recipe_id)

        # Create a detail page dynamically
        detail_page = self.create_detail_page(recipe)
        self.notebook.add(detail_page, text=f"Recipe {recipe.result_name} Details")
        self.notebook.select(detail_page)

    def create_detail_page(self, recipe):
        detail_page = ttk.Frame(self.notebook)

        recipe_label = ttk.Label(detail_page, text=recipe.result_name)
        recipe_label.pack(pady=10)

        # Create frame for ingredients tree
        ingredients_frame = ttk.Frame(detail_page)
        ingredients_frame.pack(fill=tk.BOTH, expand=True)

        # Create columns for ingredients tree
        ingredient_columns = ("Ingredient", "Quantity", "Single Price", "Stack Price", "Vendor Price")
        self.ingredients_tree = ttk.Treeview(
            ingredients_frame, columns=ingredient_columns, show="headings", selectmode="browse")

        # Set column headings and center content
        for col in ingredient_columns:
            self.ingredients_tree.heading(col, text=col)
            self.ingredients_tree.column(col, width=100, anchor=tk.CENTER, stretch=True)

        # Create list of recipe ingredient item ids
        ingredient_ids = [recipe.crystal, recipe.ingredient1, recipe.ingredient2, recipe.ingredient3,
                          recipe.ingredient4, recipe.ingredient5, recipe.ingredient6, recipe.ingredient7,
                          recipe.ingredient8]

        # Get dictionary containing the id and quantity of each non-zero ingredient id
        ingredient_counts = count_items([i for i in ingredient_ids if i > 0])

        for ingredient_id, quantity in ingredient_counts.items():
            # Get the ingredient name, replace underscores with spaces and capitalize
            ingredient_name = ItemController.get_item(ingredient_id).sort_name.replace("_", " ").title()

            # Get single and stack auction house prices, set to empty string if 0 or auction_item is None
            auction_item = AuctionController.get_auction_item(ingredient_id)
            if auction_item is None:
                single_price = ""
                stack_price = ""
            else:
                single_price = "" if auction_item.single_price == 0 else auction_item.single_price
                stack_price = "" if auction_item.stack_price == 0 else auction_item.stack_price

            # Get the cheapest vendor price, set to empty string if none found
            vendor_items = VendorController.get_vendor_items(ingredient_id)
            if vendor_items:
                cheapest_vendor_price = min([vendor_item.price for vendor_item in vendor_items])
            else:
                cheapest_vendor_price = ""

            # Insert data into the treeview
            # Set the iid to the ingredient_id for retrieval in detail view
            # Pass recipe id for updating Cost Per Synth
            self.ingredients_tree.insert("", "end", iid=ingredient_id, values=(
                ingredient_name, quantity, single_price, stack_price, cheapest_vendor_price, recipe.id))

        # Add ingredients tree to the frame
        self.ingredients_tree.pack(padx=10, pady=5, expand=True, fill="both")

        # Bind double-click to edit prices
        self.ingredients_tree.bind("<Double-1>", self.edit_ingredient_price)

        # Cost Per Synth frame
        cost_per_synth_frame = ttk.Frame(detail_page)
        cost_per_synth_frame.pack()

        # Cost Per Synth labels
        cost_per_synth_label = ttk.Label(cost_per_synth_frame, text="Cost Per Synth:")
        cost_per_synth_label.pack(side=tk.LEFT)

        self.cost_per_synth_value_label = ttk.Label(cost_per_synth_frame)
        self.cost_per_synth_value_label.pack(side=tk.LEFT)

        # Set the cost per synth value in the label
        self.update_cost_per_synth(recipe)

        # Create frame for results tree
        results_frame = ttk.Frame(detail_page)
        results_frame.pack(fill=tk.BOTH, expand=True)

        # Create columns for results tree
        result_columns = ("Result", "Single Price", "Stack Price")
        self.results_tree = ttk.Treeview(results_frame, columns=result_columns, show="headings", selectmode="browse")

        # Set column headings and center content
        for col in result_columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=100, anchor=tk.CENTER, stretch=True)

        # Create list of possible result item ids for a successful synth
        result_ids = [recipe.result, recipe.result_hq1, recipe.result_hq2, recipe.result_hq3]

        # Remove duplicates
        unique_result_ids = list(set(result_ids))

        for result_id in unique_result_ids:
            # Get the result item name, replace underscores with spaces and capitalize
            result_name = ItemController.get_item(result_id).sort_name.replace("_", " ").title()

            # Get single and stack auction house prices, set to empty string if 0 or auction_item is None
            auction_item = AuctionController.get_auction_item(result_id)
            if auction_item is None:
                single_price = ""
                stack_price = ""
            else:
                single_price = "" if auction_item.single_price == 0 else auction_item.single_price
                stack_price = "" if auction_item.stack_price == 0 else auction_item.stack_price

            # Insert data into treeview, set the iid to the result_id for easy access
            self.results_tree.insert("", "end", iid=result_id, values=(
                result_name, single_price, stack_price, recipe.id))

        # Add results tree to the frame
        self.results_tree.pack(padx=10, pady=10, expand=True, fill="both")

        # Bind double-click to edit prices
        self.results_tree.bind("<Double-1>", self.edit_result_price)

        # Close button to remove the detail tab
        close_button = ttk.Button(detail_page, text="Close", command=lambda: self.close_detail_page(detail_page))
        close_button.pack(pady=(5, 10))

        # Add more details and widgets for the recipe here
        return detail_page

    def edit_and_save_prices(self, tree, item_id, price_indices, popup_title, recipe_id):
        # Get values from the selected item
        item_values = tree.item(item_id, "values")

        # Create a popup window for editing prices
        popup = tk.Toplevel(self)
        popup.title(popup_title)

        # Calculate position relative to main window
        parent_x = self.winfo_rootx()
        parent_y = self.winfo_rooty()
        parent_width = self.winfo_width()
        parent_height = self.winfo_height()

        popup_width = 300
        popup_height = 250

        # Calculate center position
        x = parent_x + (parent_width - popup_width) // 2
        y = parent_y + (parent_height - popup_height) // 2

        # Set geometry of the popup window
        popup.geometry(f"{popup_width}x{popup_height}+{x}+{y}")

        # Label for item name
        ttk.Label(popup, text=item_values[0]).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Single price entry
        ttk.Label(popup, text="Single Price:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
        single_price_entry = ttk.Entry(popup, width=15)
        single_price_entry.insert(0, item_values[price_indices[0]])
        single_price_entry.grid(row=2, column=1, padx=10, pady=5)

        # Stack price entry
        ttk.Label(popup, text="Stack Price:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
        stack_price_entry = ttk.Entry(popup, width=15)
        stack_price_entry.insert(0, item_values[price_indices[1]])
        stack_price_entry.grid(row=3, column=1, padx=10, pady=5)

        # Save button
        save_button = ttk.Button(popup, text="Save", command=lambda: self.save_prices(
            popup, item_id, single_price_entry, stack_price_entry, tree, price_indices, recipe_id))
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

    def edit_ingredient_price(self, event):
        item_id = self.ingredients_tree.selection()[0]
        recipe_id = self.ingredients_tree.item(item_id, "values")[5]
        self.edit_and_save_prices(self.ingredients_tree, item_id, [2, 3], "Edit Ingredient Prices", recipe_id)

    def edit_result_price(self, event):
        item_id = self.results_tree.selection()[0]
        recipe_id = self.results_tree.item(item_id, "values")[3]
        self.edit_and_save_prices(self.results_tree, item_id, [1, 2], "Edit Result Prices", recipe_id)

    def save_prices(self, popup, item_id, single_price_entry, stack_price_entry, tree, price_indices, recipe_id):
        # Get updated prices from the entry boxes
        single_price = single_price_entry.get()
        stack_price = stack_price_entry.get()

        # Update values in the treeview item
        values = list(tree.item(item_id, "values"))
        values[price_indices[0]] = single_price
        values[price_indices[1]] = stack_price
        tree.item(item_id, values=values)

        # Convert empty strings to 0
        if single_price == "":
            single_price = 0
        if stack_price == "":
            stack_price = 0

        # Check if item exists in the database
        if AuctionController.auction_item_exists(item_id):
            # Update existing item
            AuctionController.update_auction_item(item_id, single_price, stack_price)
        else:
            # Insert new item
            AuctionController.add_auction_item(item_id, single_price, stack_price)

        # Get recipe from the recipe_id passed in and update Cost Per Synth
        recipe = SynthController.get_recipe(recipe_id)
        self.update_cost_per_synth(recipe)

        # Close the popup window
        popup.destroy()

    def update_cost_per_synth(self, recipe):
        # Create a synth object and calculate the cost per synth
        skill_set = Config.get_skill_set()
        crafter = Crafter(skill_set)
        synth = Synth(recipe, crafter)
        cost_per_synth = synth.calculate_cost()

        # Set Cost Per Synth Label to N/A if cost couldn't be calculated
        value_text = f"{cost_per_synth:.2f} gil" if cost_per_synth is not None else "N/A"
        self.cost_per_synth_value_label.config(text=value_text)

        # Force the UI to update
        self.update()

    def close_detail_page(self, detail_page):
        tab_id = self.notebook.index(detail_page)
        self.notebook.forget(tab_id)


# Start the main application
if __name__ == "__main__":
    app = App()
    app.mainloop()
