import tkinter as tk
from tkinter import ttk
from config import SettingsManager
from controllers import RecipeController
from entities import Recipe
from views import RecipeListPage


class ProfitPage(RecipeListPage):
    """
    A page for displaying and calculating profit information for FFXI crafting recipes.

    This class extends RecipeListPage to provide functionality specific to profit calculations,
    including custom treeview columns, recipe filtering based on profit thresholds, and
    formatted display of profit-related information.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """
        Initialize the ProfitPage.
        Sets up the action button text and initializes the parent class.

        Args:
            parent (tk.Tk): The parent Tkinter application.
        """
        self.action_button_text: str = "Generate Table"
        super().__init__(parent)

    def get_tab_text(self) -> str:
        """
        Return the text for the tab.

        Returns:
            str: The text "Profit Table" to be displayed on the tab.
        """
        return "Profit Table"

    def get_treeview_columns(self) -> list[str]:
        """
        Return the columns for the profit treeview.

        Returns:
            list[str]: A list of column identifiers for the treeview:
            ["nq", "hq", "tier", "cost_per_synth", "profit_per_synth", "profit_per_storage", "sell_freq"]
        """
        return ["nq", "hq", "tier", "cost_per_synth", "profit_per_synth", "profit_per_storage", "sell_freq"]

    def configure_treeview(self, treeview: ttk.Treeview) -> None:
        """
        Configure the treeview settings for the profit page.
        Sets up column headings and alignments for profit-related information.

        Args:
            treeview (ttk.Treeview): The treeview to configure.
        """
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

    def get_recipe_batch(self, recipe_controller: RecipeController, batch_size: int, offset: int) -> list[Recipe]:
        """
        Fetch a batch of recipes based on the user's crafting skills and skill look-ahead.
        Uses the user's craft skills and skill look-ahead settings to determine
        which recipes to fetch.

        Args:
            recipe_controller (RecipeController): The recipe controller to use.
            batch_size (int): The number of recipes to fetch.
            offset (int): The offset for pagination.

        Returns:
            list: A list of Recipe objects fetched from the RecipeController.
        """
        skills = SettingsManager.get_craft_skills()
        return recipe_controller.get_recipes_by_level(*skills, batch_size=batch_size, offset=offset)

    def should_display_recipe(self, craft_result: dict) -> bool:
        """
        Determine if a recipe should be displayed in the treeview based on profit thresholds.

        Args:
            craft_result (dict): The craft result to check.

        Returns:
            bool: True if the recipe meets all profit thresholds, False otherwise.
        """
        return self._passes_thresholds(craft_result["profit_per_synth"],
                                       craft_result["profit_per_storage"],
                                       craft_result["sell_freq"])

    def _passes_thresholds(self, profit_per_synth: int, profit_per_storage: int, sell_freq: float) -> bool:
        """
        Check if a recipe passes all profit thresholds.

        Args:
            profit_per_synth (int): The profit per synthesis.
            profit_per_storage (int): The profit per character storage unit.
            sell_freq (float): The sell frequency.

        Returns:
            bool: True if the recipe meets or exceeds all thresholds, False otherwise.
        """
        per_synth_threshold = SettingsManager.get_profit_per_synth()
        per_storage_threshold = SettingsManager.get_profit_per_storage()
        sell_freq_threshold = SettingsManager.get_sell_freq()

        return (profit_per_synth >= per_synth_threshold and
                profit_per_storage >= per_storage_threshold and
                sell_freq >= sell_freq_threshold)

    def format_row(self, craft_result: dict) -> list[any]:
        """
        Format a row for the treeview based on the craft result.

        Args:
            craft_result (dict): The craft result to format.

        Returns:
            list: A list of formatted values to display in the treeview:
            [0] NQ result (str): Formatted normal quality result
            [1] HQ results (str): Formatted high quality results
            [2] Synthesis tier (int): The tier of the synthesis
            [3] Cost per synthesis (int): The cost for each synthesis
            [4] Profit per synthesis (int): The profit for each synthesis
            [5] Profit per storage (int): The profit per character storage unit
            [6] Sell frequency (float): The sell frequency, formatted to 4 decimal places
        """
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
