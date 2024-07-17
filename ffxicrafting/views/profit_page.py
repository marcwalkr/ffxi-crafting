import threading
import tkinter as tk
from tkinter import ttk
from queue import Queue, Empty
from config.settings_manager import SettingsManager
from controllers.recipe_controller import RecipeController
from entities.crafter import Crafter
from views.recipe_list_page import RecipeListPage
from utils.widgets import TreeviewWithSort
import mysql.connector
from database.database import Database


class ProfitPage(RecipeListPage):
    def __init__(self, parent):
        super().__init__(parent)
        self.is_open = True
        self.queue = Queue()
        self.create_profit_page()
        self.check_queue()

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
        self.generate_button.config(text="Cancel", command=self.cancel_generation)
        self.clear_treeview(self.profit_tree)
        self.progress.pack_forget()
        self.progress.pack(pady=10, before=self.profit_tree)
        self.progress.start()
        self.results = []
        self.total_recipes = 0
        self.generate_thread = threading.Thread(target=self.query_recipes)
        self.generate_thread.start()

    def cancel_generation(self):
        self.is_open = False
        if hasattr(self, "generate_thread") and self.generate_thread.is_alive():
            self.generate_thread.join(timeout=1)  # Timeout to avoid long blocking
        self.generation_finished()

    def generation_finished(self):
        self.progress.stop()
        self.progress.pack_forget()
        self.generate_button.config(text="Generate Table", command=self.start_generate_profit_table)
        self.generate_button.config(state=tk.NORMAL)

    def query_recipes(self):
        try:
            skills = SettingsManager.get_skills()
            skill_look_ahead = SettingsManager.get_skill_look_ahead()
            craftable_recipes = RecipeController.get_recipes_by_level_generator(
                *(skill - skill_look_ahead for skill in skills)
            )
            for recipe in craftable_recipes:
                if not self.is_open:
                    break
                self.process_single_recipe(recipe)
            self.queue.put(self.finalize_profit_table)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.queue.put(self.generation_finished)

    def process_single_recipe(self, recipe):
        # Set price data for ingredients before calculating the cost
        for item in recipe.get_unique_ingredients():
            # None = the price has never been updated
            if (item.single_price is None or item.stack_price is None or
                    item.single_sell_freq is None or item.stack_sell_freq is None):
                item.set_auction_data()

            # Always set vendor data in case merchant settings changed
            item.set_vendor_data()

        crafter = Crafter(*SettingsManager.get_skills(), recipe)
        crafter.synth.cost = crafter.synth.calculate_cost()
        if crafter.synth.cost is not None:

            # Set price data for results before calculating profit
            for item in recipe.get_unique_results():
                # None = the price has never been updated
                if (item.single_price is None or item.stack_price is None or
                        item.single_sell_freq is None or item.stack_sell_freq is None):
                    item.set_auction_data()

            sell_freq = max(
                max(item.single_sell_freq or 0, item.stack_sell_freq or 0)
                for item in recipe.get_results()
            )

            profit_per_synth, profit_per_storage = crafter.craft(SettingsManager.get_simulation_trials())
            if self.passes_thresholds(profit_per_synth, profit_per_storage, sell_freq):
                nq_string = recipe.get_formatted_nq_result()
                hq_string = recipe.get_formatted_hq_results()

                row = [nq_string, hq_string, crafter.synth.tier,
                       crafter.synth.cost, profit_per_synth, profit_per_storage, sell_freq]
                self.results.append((recipe.id, row))
                self.queue.put(lambda: self.insert_single_into_treeview(recipe.id, row))

    def passes_thresholds(self, profit_per_synth, profit_per_storage, sell_freq):
        per_synth_threshold = SettingsManager.get_profit_per_synth()
        per_storage_threshold = SettingsManager.get_profit_per_storage()
        sell_freq_threshold = SettingsManager.get_sell_freq()

        return (profit_per_synth >= per_synth_threshold and
                profit_per_storage >= per_storage_threshold and
                sell_freq >= sell_freq_threshold)

    def finalize_profit_table(self):
        self.generation_finished()

    def insert_single_into_treeview(self, recipe_id, row):
        self.profit_tree.insert("", "end", iid=recipe_id, values=row)

    def check_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                task()
        except Empty:
            pass
        self.after(100, self.check_queue)

    def destroy(self):
        self.is_open = False
        if hasattr(self, "generate_thread") and self.generate_thread.is_alive():
            self.generate_thread.join(timeout=1)  # Timeout to avoid long blocking
        # Close all active database connections asynchronously
        threading.Thread(target=Database().close_all_connections).start()
        super().destroy()
