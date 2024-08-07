from entities import Crafter, Recipe
from config import SettingsManager


class CraftingController:
    """
    Controller class for managing crafting-related operations.

    This class handles the simulation of crafting processes, including profit calculations
    and result formatting. It serves as an intermediary between the application logic and
    the crafting entities.
    """

    def __init__(self, recipe: Recipe) -> None:
        """
        Initializes the CraftingController with a given recipe.

        Args:
            recipe (Recipe): The recipe to be simulated.
        """
        self._recipe: Recipe = recipe

    def simulate_craft(self) -> dict:
        """
        Performs a crafting simulation based on the provided recipe and the
        current crafting skill settings. It calculates profits and formats the results.

        Returns:
            dict: A dictionary containing the simulation results, including:
                - crafter (Crafter): The Crafter object used in the simulation.
                - profit_per_synth (float): The calculated profit per synthesis.
                - profit_per_storage (float): The calculated profit per storage unit.
                - sell_freq (float): The highest sell frequency among the crafting results.

            None if the crafting simulation produces no results.
        """
        skills = SettingsManager.get_craft_skills()
        crafter = Crafter(*skills, self._recipe)
        results, profit_per_synth, profit_per_storage = crafter.craft()

        if not results:
            return None

        sell_freq = max(result.get_best_sell_freq() for result in results)

        return {
            "crafter": crafter,
            "profit_per_synth": profit_per_synth,
            "profit_per_storage": profit_per_storage,
            "sell_freq": sell_freq
        }
