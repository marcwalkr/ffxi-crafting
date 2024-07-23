import tkinter as tk
from tkinter import ttk
from views import RecipeListPage
from utils import TreeviewWithSort
from controllers import RecipeController, ItemController
from entities import Crafter
from config import SettingsManager
from database import Database, DatabaseException


class SearchPage(RecipeListPage):
    def __init__(self, parent):
        self.action_button_text = "Search"
        super().__init__(parent)

    def create_widgets(self):
        self.parent.notebook.add(self, text="Search Recipes")

        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self, textvariable=self.search_var, font=("Helvetica", 14))
        self.search_entry.pack(pady=10)
        self.action_button = ttk.Button(self, text=self.action_button_text, command=self.start_process)
        self.action_button.pack(pady=(0, 10))

        self.progress_bar = ttk.Progressbar(self, mode='indeterminate', length=300)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget()

        self.treeview = TreeviewWithSort(self, columns=(
            "nq", "hq", "levels", "ingredients", "synth_cost"), show="headings")
        self.configure_treeview(self.treeview)
        self.treeview.column("synth_cost", width=0, stretch=tk.NO)  # Hide the synth_cost column

        self.treeview.pack(padx=10, pady=10, expand=True, fill="both")

        self.treeview.bind("<Double-1>", self.show_recipe_details)
        self.treeview.bind("<Button-1>", self.on_treeview_click)
        self.search_entry.bind("<Return>", lambda event: self.start_process())

    def configure_treeview(self, treeview):
        treeview.heading("nq", text="NQ")
        treeview.heading("hq", text="HQ")
        treeview.heading("levels", text="Craft Levels")
        treeview.heading("ingredients", text="Ingredients")
        treeview.column("levels", anchor=tk.CENTER)

    def query_recipes(self):
        try:
            batch_size = 25
            offset = 0
            search_finished = False

            db = Database()
            self.active_db_connections.append(db)
            recipe_controller = RecipeController(db)

            while self.is_open and not search_finished:
                results = recipe_controller.search_recipe(self.search_var.get(), batch_size, offset)

                if len(results) < batch_size:
                    search_finished = True

                self.futures.append(self.executor.submit(self.process_batch, results))

                offset += batch_size

            db.close()
            self.active_db_connections.remove(db)
        except (DatabaseException) as e:
            print(f"Error: {e}")
            self.queue.put(self.process_finished)

    def process_batch(self, results):
        db = Database()
        self.active_db_connections.append(db)
        item_controller = ItemController(db)
        try:
            for result in results:
                if not self.is_open:
                    break
                self.process_single_result(result, item_controller)
        finally:
            db.close()
            self.active_db_connections.remove(db)

    def process_single_result(self, recipe, item_controller):
        if not self.is_open:
            return

        crafter = Crafter(*SettingsManager.get_skills(), recipe)
        crafter.craft(item_controller)

        synth_cost = crafter.synth.cost if crafter.synth.cost else None

        nq_string = recipe.get_formatted_nq_result()
        hq_string = recipe.get_formatted_hq_results()
        levels_string = recipe.get_formatted_levels_string()
        ingredient_names_summarized = recipe.get_formatted_ingredient_names()

        row = [nq_string, hq_string, levels_string, ingredient_names_summarized, synth_cost]
        self.queue.put(lambda: self.insert_single_into_treeview(recipe.id, row))

    def finalize_process(self):
        self.process_finished()
