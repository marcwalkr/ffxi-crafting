from __future__ import annotations
from typing import TYPE_CHECKING
from entities import Synth, Recipe
from config import SettingsManager

if TYPE_CHECKING:
    from controllers import ItemController
    from entities import Result, Ingredient


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

    def craft(self, item_controller: ItemController) -> tuple[list[Result], float, float]:
        """
        Perform the crafting operation and calculate profits.

        Args:
            item_controller (ItemController): Controller for managing item-related operations.

        Returns:
            tuple[list[Result], float, float]: A tuple containing:
                - A list of Result objects representing the crafting outcomes.
                - The calculated profit per synthesis.
                - The calculated profit per storage slot.

        Returns (None, None, None) if the crafting cannot be performed due to missing ingredients.
        """
        num_trials = SettingsManager.get_simulation_trials()
        self._set_ingredient_costs(item_controller)
        cost = self.recipe.calculate_cost()

        if not cost:
            # The synth cannot be crafted because of missing ingredients
            return None, None, None

        results, retained_ingredients = self.synth.simulate(num_trials)
        simulation_cost = self._calculate_simulation_cost(cost, num_trials, retained_ingredients)
        cost_per_item = self._calculate_cost_per_item(simulation_cost, results)
        total_profit, total_storage_slots = self._process_results(results, cost_per_item, item_controller)

        profit_per_synth = total_profit / num_trials
        profit_per_storage = total_profit / total_storage_slots if total_storage_slots > 0 else 0

        return results.keys(), profit_per_synth, profit_per_storage

    def _set_ingredient_costs(self, item_controller: ItemController) -> None:
        """
        Update the costs of ingredients used in the recipe.

        Args:
            item_controller (ItemController): Controller for managing item-related operations.
        """
        for ingredient in self.recipe.get_unique_ingredients():
            item_controller.update_vendor_cost(ingredient.item_id)
            item_controller.update_guild_cost(ingredient.item_id)
            item_controller.update_auction_data(ingredient.item_id)

    def _calculate_simulation_cost(self, cost: int, num_trials: int, retained_ingredients: dict[Ingredient, int]) -> float:
        """
        Calculate the total cost of the crafting simulation, accounting for retained ingredients on failure.

        Args:
            cost (int): The base cost of a single crafting attempt.
            num_trials (int): The number of crafting attempts in the simulation.
            retained_ingredients (dict[Ingredient, int]): A dictionary of ingredients and their retained quantities.

        Returns:
            float: The total cost of the simulation after accounting for retained ingredients.
        """
        simulation_cost = cost * num_trials
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

    def _calculate_cost_per_item(self, simulation_cost: float, results: dict[Result, int]) -> float:
        """
        Calculate the average cost per crafted item.

        Args:
            simulation_cost (float): The total cost of the crafting simulation.
            results (dict[Result, int]): A dictionary of crafting results and their quantities.

        Returns:
            float: The average cost per crafted item. Returns 0 if no items were crafted.
        """
        total_items = sum(results.values())
        return simulation_cost / total_items if total_items > 0 else 0

    def _process_results(self, results: dict[Result, int], cost_per_item: float, item_controller: ItemController) -> tuple[float, float]:
        """
        Process the crafting results to calculate total profit and storage requirements.

        Args:
            results (dict[Result, int]): A dictionary of crafting results and their quantities.
            cost_per_item (float): The average cost per crafted item.
            item_controller (ItemController): Controller for managing item-related operations.

        Returns:
            tuple[float, float]: A tuple containing:
                - The total profit from all crafted items.
                - The total number of storage slots required for the crafted items.
        """
        total_profit = 0
        total_storage_slots = 0

        for result, quantity in results.items():
            item_controller.update_auction_data(result.item_id)

            self._calculate_result_profits(result, cost_per_item)

            total_profit += self._calculate_result_total_profit(result, quantity, cost_per_item)
            total_storage_slots += self._calculate_storage_slots(result, quantity)

        return total_profit, total_storage_slots

    def _calculate_result_profits(self, result: Result, cost_per_item: float) -> None:
        """
        Calculate and set the profit values for a single crafting result.

        Args:
            result (Result): The Result object to calculate profits for.
            cost_per_item (float): The average cost per crafted item.
        """
        result.single_profit = result.single_price - cost_per_item if result.single_price is not None else None
        if result.stack_price is not None and result.stack_size > 1:
            result.stack_profit = result.stack_price - (cost_per_item * result.stack_size)
        else:
            result.stack_profit = None

    def _calculate_result_total_profit(self, result: Result, quantity: int, cost_per_item: float) -> float:
        """
        Calculate the total profit for a specific crafting result.

        Args:
            result (Result): The Result object to calculate total profit for.
            quantity (int): The quantity of this result produced.
            cost_per_item (float): The average cost per crafted item.

        Returns:
            float: The total profit for this specific crafting result.
        """
        # If a stack price exists, use it in the calculation
        # because stacks are more commonly sold and it works as a low estimate
        if result.stack_price is not None:
            single_price_from_stack = result.stack_price / result.stack_size
            return (single_price_from_stack - cost_per_item) * quantity
        elif result.single_price is not None:
            return (result.single_price - cost_per_item) * quantity
        else:
            return (0 - cost_per_item) * quantity

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
