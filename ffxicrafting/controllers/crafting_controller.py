from __future__ import annotations
from typing import TYPE_CHECKING
from entities import Crafter, ProfitData
from config import SettingsManager

if TYPE_CHECKING:
    from entities import Recipe


class CraftingController:
    """
    Controller class for managing crafting-related operations.

    This class handles the simulation of crafting processes, including profit calculations
    and result formatting. It serves as an intermediary between the application logic and
    the crafting entities.
    """
    _profit_data_cache: dict[tuple[int, int, int, int, int, int, int, int, int], ProfitData] = {}

    @classmethod
    def get_profit_data(cls, cache_key: tuple[int, int, int, int, int, int, int, int, int]) -> ProfitData:
        """
        Get the profit data for a recipe from the cache.
        """
        if cache_key in cls._profit_data_cache:
            return cls._profit_data_cache[cache_key]
        else:
            return None

    @classmethod
    def simulate_craft(cls, recipe: Recipe) -> dict:
        """
        Performs a crafting simulation based on the provided recipe and the
        current crafting skill settings. It calculates profits and formats the results.

        Args:
            recipe (Recipe): The recipe to be simulated.

        Returns:
            dict: A dictionary containing the simulation results, including:
                - crafter (Crafter): The Crafter object used in the simulation.
                - profit_per_synth (float): The calculated profit per synthesis.
                - profit_per_storage (float): The calculated profit per storage unit.
                - sell_frequency (float): The highest sell frequency among the crafting results.

            None if the crafting simulation produces no results.
        """
        skills = SettingsManager.get_craft_skills()
        cache_key = (recipe.id, *skills)
        crafter = Crafter(*skills, recipe)
        profit_data = cls.get_profit_data(cache_key)
        if not profit_data:
            results, retained_ingredients = crafter.craft()

            if not results:
                return None

            profit_data = ProfitData(recipe, results, retained_ingredients, crafter.synth.SIMULATION_TRIALS)
            cls._profit_data_cache[cache_key] = profit_data

        sell_frequencies = [result.get_highest_sell_frequency() for result in profit_data.recipe.get_unique_results()]
        valid_frequencies = [f for f in sell_frequencies if f is not None]
        sell_frequency = max(valid_frequencies) if valid_frequencies else None

        return {
            "crafter": crafter,
            "profit_per_synth": profit_data.profit_per_synth,
            "profit_per_storage": profit_data.profit_per_storage,
            "sell_frequency": sell_frequency
        }
