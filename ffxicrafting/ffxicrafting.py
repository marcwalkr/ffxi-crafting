import tkinter as tk
from tkinter import ttk
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from helpers import summarize_list


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FFXI Crafting Tool")
        self.geometry("800x600")

        # Configure styles
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 14), padding=10)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10), padding=4)

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
        search_entry.pack(pady=5)
        search_button = ttk.Button(self.search_page, text="Search",
                                   command=lambda: self.search_recipes(search_var.get()))
        search_button.pack()

        self.tree = ttk.Treeview(self.search_page, columns=("item", "levels", "ingredients"), show="headings")
        self.tree.heading("item", text="Item")
        self.tree.heading("levels", text="Craft Levels")
        self.tree.heading("ingredients", text="Ingredients")
        self.tree.pack(expand=True, fill="both")
        self.tree.bind("<Double-1>", self.show_recipe_details)

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
        for i in self.tree.get_children():
            self.tree.delete(i)

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

            self.tree.insert("", "end", values=tree_values)

    def show_recipe_details(self, event):
        item = self.tree.selection()[0]
        recipe_item = self.tree.item(item, "values")[0]
        # Create a detail page dynamically
        detail_page = self.create_detail_page(recipe_item)
        self.notebook.add(detail_page, text=f"Recipe {recipe_item} Details")
        self.notebook.select(detail_page)

    def create_detail_page(self, recipe_item):
        detail_page = ttk.Frame(self.notebook)

        detail_label = ttk.Label(detail_page, text=f"Details for Recipe {recipe_item}")
        detail_label.pack(pady=20)

        # Close button to remove the detail tab
        close_button = ttk.Button(detail_page, text="Close", command=lambda: self.close_detail_page(detail_page))
        close_button.pack(pady=10)

        # Add more details and widgets for the recipe here
        return detail_page

    def close_detail_page(self, detail_page):
        tab_id = self.notebook.index(detail_page)
        self.notebook.forget(tab_id)


# Start the main application
if __name__ == "__main__":
    app = App()
    app.mainloop()
