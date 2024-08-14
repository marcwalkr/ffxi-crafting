from __future__ import annotations
from typing import TYPE_CHECKING
from entities import Crafter, SimulationData
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
    _simulation_data_cache: dict[tuple[int, int, int, int, int, int, int, int, int], SimulationData] = {}

    @classmethod
    def get_simulation_data(cls, cache_key: tuple[int, int, int, int, int, int, int, int, int]) -> SimulationData:
        """
        Get the simulation data for a recipe from the cache.
        """
        if cache_key in cls._simulation_data_cache:
            return cls._simulation_data_cache[cache_key]
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
        simulation_data = cls.get_simulation_data(cache_key)
        if not simulation_data:
            results, retained_ingredients = crafter.craft()

            if not results:
                return None

            simulation_data = SimulationData(recipe, results, retained_ingredients, crafter.synth.SIMULATION_TRIALS)
            cls._simulation_data_cache[cache_key] = simulation_data

        sell_frequencies = [result.get_highest_sell_frequency() for result in simulation_data.recipe.get_unique_results()]
        valid_frequencies = [f for f in sell_frequencies if f is not None]
        sell_frequency = max(valid_frequencies) if valid_frequencies else None

        return {
            "crafter": crafter,
            "profit_per_synth": simulation_data.profit_per_synth,
            "profit_per_storage": simulation_data.profit_per_storage,
            "sell_frequency": sell_frequency
        }
