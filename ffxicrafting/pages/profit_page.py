import threading
import tkinter as tk
from tkinter import ttk
from config.settings_manager import SettingsManager
from controllers.recipe_controller import RecipeController
from entities.crafter import Crafter
from pages.recipe_list_page import RecipeListPage
from utils.widgets import TreeviewWithSort


class ProfitPage(RecipeListPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_open = True
        self.create_profit_page()

    def create_profit_page(self):
        self.parent.notebook.add(self, text="Profit Table")
        self.generate_button = ttk.Button(self, text="Generate Table", command=self.start_generate_profit_table)
        self.generate_button.pack(pady=10)

        self.progress = ttk.Progressbar(self, mode='indeterminate', length=300)
        self.progress.pack(pady=10)
        self.progress.pack_forget()

        self.profit_tree = TreeviewWithSort(self, columns=("nq", "hq", "tier", "cost_per_synth", "profit_per_synth",
                                                           "profit_per_storage", "sell_freq"), show="headings")
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
        treeview.heading("sell_freq", text="Sell Freq")

        treeview.column("tier", anchor=tk.CENTER)
        treeview.column("cost_per_synth", anchor=tk.CENTER)
        treeview.column("profit_per_synth", anchor=tk.CENTER)
        treeview.column("profit_per_storage", anchor=tk.CENTER)
        treeview.column("sell_freq", anchor=tk.CENTER)

    def start_generate_profit_table(self):
        self.generate_button.config(state=tk.DISABLED)
        self.clear_treeview(self.profit_tree)
        self.progress.pack_forget()
        self.progress.pack(pady=10, before=self.profit_tree)
        self.progress.start()
        self.results = []
        self.total_recipes = 0
        self.generate_thread = threading.Thread(target=self.query_recipes)
        self.generate_thread.start()

    def query_recipes(self):
        skills = SettingsManager.get_skills()
        skill_look_ahead = SettingsManager.get_skill_look_ahead()
        for recipe in RecipeController.get_recipes_by_craft_levels_generator(*(skill - skill_look_ahead for skill in skills)):
            if not self.is_open:
                return
            self.process_single_recipe(recipe)
        self.finalize_profit_table()

    def process_single_recipe(self, recipe):
        crafter = Crafter(*SettingsManager.get_skills(), recipe)
        crafter.synth.cost = crafter.synth.calculate_cost()
        if crafter.synth.cost is not None:
            profit_per_synth, profit_per_storage = crafter.craft(SettingsManager.get_simulation_trials())
            if profit_per_synth >= SettingsManager.get_profit_per_synth() and profit_per_storage >= SettingsManager.get_profit_per_storage():
                nq_string = recipe.get_formatted_nq_result()
                hq_string = recipe.get_formatted_hq_results()

                for item in recipe.get_unique_ingredients():
                    item.set_auction_data()
                    item.set_vendor_data()

                for item in recipe.get_unique_results():
                    item.set_auction_data()

                sell_freq = max(
                    max(item.single_sell_freq, item.stack_sell_freq)
                    for item in recipe.get_results()
                )
                row = [nq_string, hq_string, crafter.synth.tier,
                       crafter.synth.cost, profit_per_synth, profit_per_storage, sell_freq]
                self.results.append((recipe.id, row))
                self.after(0, self.insert_single_into_treeview, recipe.id, row)

    def finalize_profit_table(self):
        self.after(0, self.generation_finished)

    def generation_finished(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.generate_button.config(state=tk.NORMAL)

    def insert_single_into_treeview(self, recipe_id, row):
        self.profit_tree.insert("", "end", iid=recipe_id, values=row)

    def destroy(self):
        self.is_open = False
        if hasattr(self, "generate_thread") and self.generate_thread.is_alive():
            self.generate_thread.join()
        super().destroy()
