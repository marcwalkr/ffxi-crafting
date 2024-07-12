import tkinter as tk
from tkinter import ttk


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

        self.listbox = tk.Listbox(self.search_page, font=("Helvetica", 14))
        self.listbox.pack(expand=True, fill="both")
        self.listbox.bind("<<ListboxSelect>>", self.show_recipe_details)

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
        # Clear the listbox and perform the search
        self.listbox.delete(0, tk.END)
        # Example search results (replace with actual database query)
        results = [("1: Potion of Healing (Level 10)",), ("2: Elixir of Strength (Level 15)",)]
        for result in results:
            self.listbox.insert(tk.END, result[0])

    def show_recipe_details(self, event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            item = event.widget.get(index)
            recipe_id = int(item.split(":")[0])
            # Create a detail page dynamically
            detail_page = self.create_detail_page(recipe_id)
            self.notebook.add(detail_page, text=f"Recipe {recipe_id} Details")
            self.notebook.select(detail_page)

    def create_detail_page(self, recipe_id):
        detail_page = ttk.Frame(self.notebook)

        detail_label = ttk.Label(detail_page, text=f"Details for Recipe {recipe_id}")
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
