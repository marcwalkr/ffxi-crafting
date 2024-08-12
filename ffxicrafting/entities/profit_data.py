from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from entities import Item, Recipe


class ProfitData:
    """
    Class to store profit data for a crafting simulation.
    """

    def __init__(self, recipe: Recipe, results: dict[Item, int], retained_ingredients: dict[Item, int],
                 num_trials: int) -> None:
        """
        Initialize the ProfitData object.

        Args:
            recipe (Recipe): The recipe that was used to craft the results.
            results (dict[Item, int]): A dictionary of crafted items and their quantities.
            retained_ingredients (dict[Item, int]): A dictionary of items and their retained quantities.
            num_trials (int): The number of trials used in the simulation.
        """
        simulation_cost = self._calculate_simulation_cost(recipe.min_cost, retained_ingredients, num_trials)
        total_revenue, total_storage_slots = self._process_results(results)
        total_profit = total_revenue - simulation_cost

        self.recipe = recipe
        self.profit_per_synth: float = total_profit / num_trials
        self.profit_per_storage: float = total_profit / total_storage_slots if total_storage_slots > 0 else 0
        self.proportions: dict[Item, float] = self._get_proportions(results)
        self.profit_contributions: dict[Item, float] = self._get_profit_contributions(results, simulation_cost,
                                                                                      total_profit)

    def _calculate_simulation_cost(self, cost: float, retained_ingredients: dict[Item, int], num_trials: int) -> float:
        """
        Calculate the total cost of the crafting simulation, accounting for retained ingredients on failure.

        Args:
            cost (float): The base cost of a single crafting attempt.
            retained_ingredients (dict[Item, int]): A dictionary of items and their retained quantities.
            num_trials (int): The number of trials used in the simulation.
        Returns:
            float: The total cost of the simulation after accounting for retained ingredients.
        """
        simulation_cost = cost * num_trials
        saved_cost = self._get_saved_cost(retained_ingredients)
        return simulation_cost - saved_cost

    def _get_saved_cost(self, retained_ingredients: dict[Item, int]) -> float:
        """
        Calculate the cost saved from retained ingredients on failure.

        Args:
            retained_ingredients (dict[Item, int]): A dictionary of items and their retained quantities.

        Returns:
            float: The total cost saved from retained ingredients.
        """
        total_saved_cost = 0
        for ingredient, quantity in retained_ingredients.items():
            min_cost = ingredient.get_min_cost()
            saved_cost = min_cost * quantity
            total_saved_cost += saved_cost

        return total_saved_cost

    def _get_proportions(self, results: dict[Item, int]) -> dict[Item, float]:
        """
        Get the proportion each result makes up in the overall recipe results.

        Args:
            results (dict[Item, int]): A dictionary of items and their quantities.
        """
        total_items_produced = sum(results.values())
        proportions = {}
        for result, quantity in results.items():
            proportions[result] = quantity / total_items_produced

        return proportions

    def _process_results(self, results: dict[Item, int]) -> tuple[float, float]:
        """
        Process the crafting results to calculate total revenue and storage requirements.

        Args:
            results (dict[Item, int]): A dictionary of items and their quantities.

        Returns:
            tuple[float, float]: A tuple containing:
                - The total revenue from all crafted items.
                - The total number of storage slots required for the crafted items.
        """
        total_revenue = 0
        total_storage_slots = 0

        for result, quantity in results.items():
            total_revenue += self._calculate_result_total_revenue(result, quantity)
            total_storage_slots += self._calculate_storage_slots(result, quantity)

        return total_revenue, total_storage_slots

    def _calculate_result_total_revenue(self, result: Item, quantity: int) -> float:
        """
        Calculate the total revenue for a specific crafting result.
        Uses the fastest selling form of the item to calculate the revenue.

        Args:
            result (Item): The Item object to calculate total revenue for.
            quantity (int): The quantity of this result produced.

        Returns:
            float: The total revenue for this specific crafting result.
        """
        fastest_selling_price = result.get_fastest_selling_price_per_unit()
        if fastest_selling_price is not None:
            return fastest_selling_price * quantity
        else:
            return 0

    def _calculate_storage_slots(self, result: Item, quantity: int) -> int:
        """
        Calculate the number of storage slots required for a specific crafting result.

        Args:
            result (Item): The Item object to calculate storage for.
            quantity (int): The quantity of this result produced.

        Returns:
            int: The number of storage slots required for this crafting result.
        """
        return (quantity + result.stack_size - 1) // result.stack_size

    def _get_profit_contributions(self, results: dict[Item, int], simulation_cost: float,
                                  total_profit: float) -> dict[Item, float]:
        """
        Set the profit contribution for each result.

        Args:
            results (dict[Item, int]): A dictionary of items and their quantities.
            simulation_cost (float): The total cost of the crafting simulation.
            total_profit (float): The total profit from all crafted items.

        Returns:
            dict[Item, float]: A dictionary of items and their profit contributions.
        """
        total_items = sum(results.values())
        cost_per_item = simulation_cost / total_items

        # Calculate the total profit from each result
        result_profits = {}
        for result, quantity in results.items():
            fastest_selling_price = result.get_fastest_selling_price_per_unit()
            if fastest_selling_price is not None:
                result_profit = (fastest_selling_price - cost_per_item) * quantity
                result_profits[result] = result_profit
            else:
                result_profits[result] = 0

        profit_contributions = {}

        # Handle cases where total profit is zero or negative
        if total_profit <= 0:
            # If total profit is zero or negative, contributions cannot be calculated meaningfully
            for result in results.keys():
                profit_contributions[result] = 0
        else:
            # Calculate profit contributions
            for result, profit in result_profits.items():
                if profit > 0:
                    profit_contributions[result] = profit / total_profit
                else:
                    profit_contributions[result] = 0

        # Adjustments for contributions that add up to more or less than 1 due to rounding errors
        if total_profit > 0:
            total_contribution = sum(profit_contributions.values())
            if total_contribution != 1:
                # Adjust contributions proportionally if necessary
                adjustment_factor = 1 / total_contribution
                for result in profit_contributions.keys():
                    profit_contributions[result] *= adjustment_factor

        return profit_contributions
