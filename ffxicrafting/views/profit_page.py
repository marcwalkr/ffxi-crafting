import tkinter as tk
from tkinter import ttk
from views import RecipeListPage
from utils import TreeviewWithSort
from controllers import RecipeController, ItemController
from entities import Crafter
from config import SettingsManager
from database import Database, DatabaseException


class ProfitPage(RecipeListPage):
    def __init__(self, parent):
        self.action_button_text = "Generate Table"
        super().__init__(parent)

    def create_widgets(self):
        self.parent.notebook.add(self, text="Profit Table")
        self.action_button = ttk.Button(self, text=self.action_button_text, command=self.start_process)
        self.action_button.pack(pady=10)

        self.progress_bar = ttk.Progressbar(self, mode='indeterminate', length=300)
        self.progress_bar.pack(pady=10)
        self.progress_bar.pack_forget()

        self.treeview = TreeviewWithSort(self, columns=("nq", "hq", "tier", "cost_per_synth", "profit_per_synth",
                                                        "profit_per_storage", "sell_freq"), show="headings")
        self.configure_treeview(self.treeview)
        self.treeview.pack(padx=10, pady=10, expand=True, fill="both")

        self.treeview.bind("<Double-1>", self.show_recipe_details)
        self.treeview.bind("<Button-1>", self.on_treeview_click)

    def configure_treeview(self, treeview):
        treeview.heading("nq", text="NQ")
        treeview.heading("hq", text="HQ")
        treeview.heading("tier", text="Tier")
        treeview.heading("cost_per_synth", text="Cost / Synth")
        treeview.heading("profit_per_synth", text="Profit / Synth")
        treeview.heading("profit_per_storage", text="Profit / Storage")
        treeview.heading("sell_freq", text="Sell Freq")

        treeview.column("tier", anchor=tk.CENTER)
        treeview.column("cost_per_synth", anchor=tk.CENTER)
        treeview.column("profit_per_synth", anchor=tk.CENTER)
        treeview.column("profit_per_storage", anchor=tk.CENTER)
        treeview.column("sell_freq", anchor=tk.CENTER)

    def query_recipes(self):
        try:
            skills = SettingsManager.get_skills()
            skill_look_ahead = SettingsManager.get_skill_look_ahead()

            batch_size = 25
            offset = 0
            search_finished = False

            db = Database()
            self.active_db_connections.append(db)
            recipe_controller = RecipeController(db)

            while self.is_open and not search_finished:
                craftable_recipes = recipe_controller.get_recipes_by_level(
                    *(skill - skill_look_ahead for skill in skills), batch_size=batch_size, offset=offset
                )

                if len(craftable_recipes) < batch_size:
                    search_finished = True

                self.futures.append(self.executor.submit(self.process_batch, craftable_recipes))

                offset += batch_size

            db.close()
            self.active_db_connections.remove(db)
        except (DatabaseException) as e:
            print(f"Error: {e}")
            self.queue.put(self.process_finished)

    def process_batch(self, craftable_recipes):
        db = Database()
        self.active_db_connections.append(db)
        item_controller = ItemController(db)
        try:
            for recipe in craftable_recipes:
                if not self.is_open:
                    break
                self.process_single_recipe(recipe, item_controller)
        finally:
            db.close()
            self.active_db_connections.remove(db)

    def process_single_recipe(self, recipe, item_controller):
        if not self.is_open:
            return

        crafter = Crafter(*SettingsManager.get_skills(), recipe)
        results, profit_per_synth, profit_per_storage = crafter.craft(item_controller)

        if not results:
            return

        sell_freq = max(
            max(result.single_sell_freq or 0, result.stack_sell_freq or 0)
            for result in results
        )

        if self.passes_thresholds(profit_per_synth, profit_per_storage, sell_freq):
            nq_string = recipe.get_formatted_nq_result()
            hq_string = recipe.get_formatted_hq_results()

            row = [nq_string, hq_string, crafter.synth.tier, crafter.synth.cost, profit_per_synth, profit_per_storage,
                   sell_freq, crafter.synth.cost]
            self.queue.put(lambda: self.insert_single_into_treeview(recipe.id, row))

    def passes_thresholds(self, profit_per_synth, profit_per_storage, sell_freq):
        per_synth_threshold = SettingsManager.get_profit_per_synth()
        per_storage_threshold = SettingsManager.get_profit_per_storage()
        sell_freq_threshold = SettingsManager.get_sell_freq()

        return (profit_per_synth >= per_synth_threshold and
                profit_per_storage >= per_storage_threshold and
                sell_freq >= sell_freq_threshold)

    def finalize_process(self):
        self.process_finished()
