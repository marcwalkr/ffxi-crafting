import tkinter as tk
from views import RecipeListPage
from config import SettingsManager


class ProfitPage(RecipeListPage):
    def __init__(self, parent):
        self.action_button_text = "Generate Table"
        super().__init__(parent)

    def get_tab_text(self):
        return "Profit Table"

    def get_treeview_columns(self):
        return ("nq", "hq", "tier", "cost_per_synth", "profit_per_synth", "profit_per_storage", "sell_freq")

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

    def get_recipe_batch(self, batch_size, offset):
        skills = SettingsManager.get_craft_skills()
        skill_look_ahead = SettingsManager.get_skill_look_ahead()
        return self.recipe_controller.get_recipes_by_level(
            *(skill - skill_look_ahead for skill in skills), batch_size=batch_size, offset=offset
        )

    def should_display_recipe(self, craft_result):
        return self.passes_thresholds(craft_result["profit_per_synth"],
                                      craft_result["profit_per_storage"],
                                      craft_result["sell_freq"])

    def passes_thresholds(self, profit_per_synth, profit_per_storage, sell_freq):
        per_synth_threshold = SettingsManager.get_profit_per_synth()
        per_storage_threshold = SettingsManager.get_profit_per_storage()
        sell_freq_threshold = SettingsManager.get_sell_freq()

        return (profit_per_synth >= per_synth_threshold and
                profit_per_storage >= per_storage_threshold and
                sell_freq >= sell_freq_threshold)

    def format_row(self, craft_result):
        crafter = craft_result["crafter"]

        return [
            crafter.recipe.get_formatted_nq_result(),
            crafter.recipe.get_formatted_hq_results(),
            crafter.synth.tier,
            int(crafter.recipe.cost),
            int(craft_result["profit_per_synth"]),
            int(craft_result["profit_per_storage"]),
            float(f"{craft_result['sell_freq']:.4f}")
        ]
