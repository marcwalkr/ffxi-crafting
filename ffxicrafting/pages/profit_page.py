import tkinter as tk
from tkinter import ttk
import threading
from utils.widgets import TreeviewWithSort
from controllers.recipe_controller import RecipeController
from entities.crafter import Crafter
from config.settings_manager import SettingsManager
from pages.recipe_list_page import RecipeListPage


class ProfitPage(RecipeListPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_profit_page()

    def create_profit_page(self):
        self.parent.notebook.add(self, text="Profit Table")

        self.generate_button = ttk.Button(self, text="Generate Table", command=self.start_generate_profit_table)
        self.generate_button.pack(pady=10)

        self.profit_tree = TreeviewWithSort(self, columns=(
            "nq", "hq", "tier", "cost_per_synth", "profit_per_synth", "profit_per_storage", "sell_freq"), show="headings")
        self.configure_profit_treeview(self.profit_tree)
        self.profit_tree.pack(padx=10, pady=10, expand=True, fill="both")

        self.profit_tree.bind("<Double-1>", self.show_recipe_details)
        self.profit_tree.bind("<Button-1>", self.on_treeview_click)

    def start_generate_profit_table(self):
        self.generate_button.config(state=tk.DISABLED)
        self.clear_treeview(self.profit_tree)
        self.progress.pack_forget()
        self.progress.pack(pady=10, before=self.profit_tree)
        self.progress.start()
        threading.Thread(target=self.query_recipes).start()

    def query_recipes(self):
        skills = SettingsManager.get_skills()
        skill_look_ahead = SettingsManager.get_skill_look_ahead()
        recipes = RecipeController.get_recipes_by_craft_levels(*(skill - skill_look_ahead for skill in skills))
        self.synth_profit_threshold = SettingsManager.get_profit_per_synth()
        self.storage_profit_threshold = SettingsManager.get_profit_per_storage()
        self.simulation_trials = SettingsManager.get_simulation_trials()
        self.total_recipes = len(recipes)
        self.recipes = recipes
        self.after(10, self.update_profit_progress, 0, [])

    def update_profit_progress(self, index, batch):
        if index < self.total_recipes:
            recipe = self.recipes[index]
            crafter = Crafter(*SettingsManager.get_skills(), recipe)

            crafter.synth.cost = crafter.synth.calculate_cost()
            if crafter.synth.cost is not None:
                profit_per_synth, profit_per_storage = crafter.craft(self.simulation_trials)
                if profit_per_synth >= self.synth_profit_threshold and profit_per_storage >= self.storage_profit_threshold:
                    nq_string = recipe.get_formatted_nq_result()
                    hq_string = recipe.get_formatted_hq_results()
                    row = [nq_string, hq_string, crafter.synth.tier,
                           crafter.synth.cost, profit_per_synth, profit_per_storage]
                    batch.append((recipe.id, row))

            if len(batch) >= 10:
                for item in batch:
                    self.profit_tree.insert("", "end", iid=item[0], values=item[1])
                batch.clear()

            self.after(10, self.update_profit_progress, index + 1, batch)
        else:
            for item in batch:
                self.profit_tree.insert("", "end", iid=item[0], values=item[1])
            self.progress.stop()
            self.progress.pack_forget()
            self.generate_button.config(state=tk.NORMAL)

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

            # Get the maximum sell frequency of all results
            sell_freq = max(
                max(item.single_sell_freq, item.stack_sell_freq)
                for item in recipe.get_results()
            )

            row = [nq_string, hq_string, crafter.synth.tier,
                   crafter.synth.cost, profit_per_synth, profit_per_storage, sell_freq]
            self.profit_tree.insert("", "end", iid=recipe.id, values=row)
