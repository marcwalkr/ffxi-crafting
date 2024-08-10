from __future__ import annotations
from typing import TYPE_CHECKING
from entities import Synth

if TYPE_CHECKING:
    from entities import Result, Ingredient, Recipe


class Crafter:
    """
    Represents a crafter in the game, capable of performing synthesis operations.
    """

    def __init__(self, wood: int, smith: int, gold: int, cloth: int, leather: int, bone: int, alchemy: int, cook: int,
                 recipe: Recipe) -> None:
        """
        Initialize a Crafter instance with crafting skills and a recipe.

        Args:
            wood (int): Woodworking crafting skill level.
            smith (int): Smithing crafting skill level.
            gold (int): Goldsmithing crafting skill level.
            cloth (int): Clothcraft crafting skill level.
            leather (int): Leatherworking crafting skill level.
            bone (int): Bonecraft crafting skill level.
            alchemy (int): Alchemy crafting skill level.
            cook (int): Cooking crafting skill level.
            recipe (Recipe): The recipe to be crafted.
        """
        self.wood: int = wood
        self.smith: int = smith
        self.gold: int = gold
        self.cloth: int = cloth
        self.leather: int = leather
        self.bone: int = bone
        self.alchemy: int = alchemy
        self.cook: int = cook
        self.recipe: Recipe = recipe
        self.synth: Synth = Synth(recipe, self)

    def craft(self) -> tuple[list[Result], float, float]:
        """
        Perform the crafting operation and calculate profits.

        Returns:
            tuple[list[Result], float, float]: A tuple containing:
                - A list of Result objects representing the crafting outcomes.
                - The calculated profit per synthesis.
                - The calculated profit per storage slot.

        Returns (None, None, None) if the crafting cannot be performed due to missing ingredients.
        """
        cost = self.recipe.calculate_cost()

        if not cost:
            # The synth cannot be crafted because of missing ingredients
            return None, None, None

        results, retained_ingredients = self.synth.simulate()
        self._set_proportions(results)
        simulation_cost = self._calculate_simulation_cost(cost, retained_ingredients)
        self._set_crafted_costs(simulation_cost, results)
        total_revenue, total_storage_slots = self._process_results(results)

        total_profit = total_revenue - simulation_cost
        self._set_profit_contributions(results, simulation_cost, total_profit)

        profit_per_synth = total_profit / self.synth.SIMULATION_TRIALS
        profit_per_storage = total_profit / total_storage_slots if total_storage_slots > 0 else 0

        return results.keys(), profit_per_synth, profit_per_storage

    def _calculate_simulation_cost(self, cost: float, retained_ingredients: dict[Ingredient, int]) -> float:
        """
        Calculate the total cost of the crafting simulation, accounting for retained ingredients on failure.

        Args:
            cost (float): The base cost of a single crafting attempt.
            retained_ingredients (dict[Ingredient, int]): A dictionary of ingredients and their retained quantities.

        Returns:
            float: The total cost of the simulation after accounting for retained ingredients.
        """
        simulation_cost = cost * self.synth.SIMULATION_TRIALS
        saved_cost = self._get_saved_cost(retained_ingredients)
        return simulation_cost - saved_cost

    def _get_saved_cost(self, retained_ingredients: dict[Ingredient, int]) -> float:
        """
        Calculate the cost saved from retained ingredients on failure.

        Args:
            retained_ingredients (dict[Ingredient, int]): A dictionary of ingredients and their retained quantities.

        Returns:
            float: The total cost saved from retained ingredients.
        """
        total_saved_cost = 0
        for ingredient, quantity in retained_ingredients.items():
            min_cost = ingredient.get_min_cost()
            saved_cost = min_cost * quantity
            total_saved_cost += saved_cost

        return total_saved_cost

    def _set_proportions(self, results: dict[Result, int]) -> None:
        """
        Set the craft rates for each result.

        Args:
            results (dict[Result, int]): A dictionary of crafting results and their quantities.
        """
        total_items_produced = sum(results.values())
        for result, quantity in results.items():
            result.proportion = quantity / total_items_produced

    def _set_crafted_costs(self, simulation_cost: float, results: dict[Result, int]) -> None:
        """
        Set the crafted cost for each result, the cost to craft a single unit of the item.

        Args:
            simulation_cost (float): The total cost of the crafting simulation.
            results (dict[Result, int]): A dictionary of crafting results and their quantities.
        """
        for result, quantity in results.items():
            result.crafted_cost = simulation_cost / quantity

    def _process_results(self, results: dict[Result, int]) -> tuple[float, float]:
        """
        Process the crafting results to calculate total revenue and storage requirements.

        Args:
            results (dict[Result, int]): A dictionary of crafting results and their quantities.

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

    def _calculate_result_total_revenue(self, result: Result, quantity: int) -> float:
        """
        Calculate the total revenue for a specific crafting result.
        Uses the fastest selling form of the item to calculate the revenue.

        Args:
            result (Result): The Result object to calculate total revenue for.
            quantity (int): The quantity of this result produced.

        Returns:
            float: The total revenue for this specific crafting result.
        """
        fastest_selling_price = result.get_fastest_selling_price_per_unit()
        if fastest_selling_price is not None:
            return fastest_selling_price * quantity
        else:
            return 0

    def _calculate_storage_slots(self, result: Result, quantity: int) -> int:
        """
        Calculate the number of storage slots required for a specific crafting result.

        Args:
            result (Result): The Result object to calculate storage for.
            quantity (int): The quantity of this result produced.

        Returns:
            int: The number of storage slots required for this crafting result.
        """
        return (quantity + result.stack_size - 1) // result.stack_size

    def _set_profit_contributions(self, results: dict[Result, int], simulation_cost: float, total_profit: float) -> None:
        """
        Set the profit contribution for each result.

        Args:
            results (dict[Result, int]): A dictionary of crafting results and their quantities.
            simulation_cost (float): The total cost of the crafting simulation.
            total_profit (float): The total profit from all crafted items.
        """
        cost_per_item = simulation_cost / sum(results.values())

        # Calculate the total profit from each result
        result_profits = {}
        for result, quantity in results.items():
            fastest_selling_price = result.get_fastest_selling_price_per_unit()
            if fastest_selling_price is not None:
                result_profit = (fastest_selling_price - cost_per_item) * quantity
                result_profits[result] = result_profit
            else:
                result_profits[result] = 0

        # Handle cases where total profit is zero or negative
        if total_profit <= 0:
            # If total profit is zero or negative, contributions cannot be calculated meaningfully
            for result in results.keys():
                result.profit_contribution = 0
        else:
            # Calculate profit contributions
            for result, profit in result_profits.items():
                if profit > 0:
                    result.profit_contribution = profit / total_profit
                else:
                    result.profit_contribution = 0

        # Adjustments for contributions that add up to more or less than 1 due to rounding errors
        if total_profit > 0:
            total_contribution = sum(result.profit_contribution for result in results.keys())
            if total_contribution != 1:
                # Adjust contributions proportionally if necessary
                adjustment_factor = 1 / total_contribution
                for result in results.keys():
                    result.profit_contribution *= adjustment_factor
