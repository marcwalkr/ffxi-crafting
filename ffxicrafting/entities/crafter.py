from __future__ import annotations
from typing import TYPE_CHECKING
from entities import Synth, Recipe
from config import SettingsManager

if TYPE_CHECKING:
    from controllers import ItemController
    from entities import Result


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

        Simulates the crafting process, calculates profits, and updates result information.

        Args:
            item_controller (ItemController): Controller for managing item-related operations.

        Returns:
            tuple[list[Result], float, float]: A tuple containing:
                - A list of Result objects representing the crafting outcomes.
                - The calculated profit per synthesis.
                - The calculated profit per character storage unit.

        Returns ([], None, None) if the simulation produces no results or cost.
        """
        num_trials = SettingsManager.get_simulation_trials()
        simulation_cost, results = self.synth.simulate(num_trials, item_controller)

        if not simulation_cost or not results:
            return [], None, None

        # Calculate and set the expected profit for each result, selling them as singles and stacks
        self._set_results_profit(results, simulation_cost, item_controller)

        # Calculate the overall expected profit per synth and per character storage unit
        profit_per_synth = self._get_profit_per_synth(results, simulation_cost, num_trials)
        profit_per_storage = self._get_profit_per_storage(results, simulation_cost)

        return results.keys(), profit_per_synth, profit_per_storage

    def _set_results_profit(self, results: dict[Result, int], simulation_cost: float, item_controller: ItemController) -> None:
        """
        Calculate and set the profit for each crafting result.

        Args:
            results (dict[Result, int]): Dictionary of Results and their quantities.
            simulation_cost (float): The total cost of the crafting simulation.
            item_controller (ItemController): Controller for managing item-related operations.
        """
        for result, quantity in results.items():
            item_controller.update_auction_data(result.item_id)
            result.crafted_cost = simulation_cost / quantity
            result.single_profit = self._get_single_profit(result, result.crafted_cost)
            result.stack_profit = self._get_stack_profit(result, result.crafted_cost)

    def _get_single_profit(self, result: Result, crafted_cost: float) -> float:
        """
        Calculate the profit for selling a single item.

        Args:
            result (Result): The Result object representing the crafted item.
            crafted_cost (float): The cost to craft a single item.

        Returns:
            float: The calculated profit for selling a single item.
        """
        return self._calculate_profit(result, crafted_cost, single=True)

    def _get_stack_profit(self, result: Result, crafted_cost: float) -> float:
        """
        Calculate the profit for selling a stack of items.

        Args:
            result (Result): The Result object representing the crafted item.
            crafted_cost (float): The cost to craft a single item.

        Returns:
            float: The calculated profit for selling a stack of items.
        """
        return self._calculate_profit(result, crafted_cost, single=False)

    def _calculate_profit(self, result: Result, crafted_cost: float, single: bool = True) -> float:
        """
        Calculate the profit for selling an item, either as a single item or as a stack.

        Args:
            result (Result): The Result object representing the crafted item.
            crafted_cost (float): The cost to craft a single item.
            single (bool, optional): If True, calculate for a single item. If False, calculate for a stack. Defaults to True.

        Returns:
            float: The calculated profit. Returns None if the selling price is not available.
        """
        price = result.single_price if single else result.stack_price
        stack_size = result.stack_size

        if price is None:
            return None

        if single:
            profit = price - crafted_cost
        else:
            cost_per_stack = crafted_cost * stack_size
            profit = price - cost_per_stack

        return profit

    def _get_profit_per_synth(self, results: dict[Result, int], simulation_cost: float, num_trials: int) -> float:
        """
        Calculate the average profit per synthesis operation.

        Args:
            results (dict[Result, int]): Dictionary of Results and their quantities.
            simulation_cost (float): The total cost of the crafting simulation.
            num_trials (int): The number of synthesis trials performed in the simulation.

        Returns:
            float: The calculated average profit per synthesis.
        """
        total_profit = self._calculate_total_profit(results, simulation_cost)
        profit_per_synth = total_profit / num_trials
        return profit_per_synth

    def _get_profit_per_storage(self, results: dict[Result, int], simulation_cost: float) -> float:
        """
        Calculate the profit per character storage unit.

        Args:
            results (dict[Result, int]): Dictionary of Results and their quantities.
            simulation_cost (float): The total cost of the crafting simulation.

        Returns:
            float: The calculated profit per character storage unit. Returns 0 if total storage is 0.
        """
        total_profit = self._calculate_total_profit(results, simulation_cost)
        total_storage = self._calculate_total_storage(results)
        profit_per_storage = total_profit / total_storage if total_storage > 0 else 0
        return profit_per_storage

    def _calculate_total_profit(self, results: dict[Result, int], simulation_cost: float) -> float:
        """
        Calculate the total profit from all crafting results.

        Args:
            results (dict[Result, int]): Dictionary of Results and their quantities.
            simulation_cost (float): The total cost of the crafting simulation.

        Returns:
            float: The calculated total profit.
        """
        total_gil = 0
        for result, quantity in results.items():
            # If a stack price exists, use it in the calculation because stacks are more commonly sold
            # and it works as a low estimate
            single_price = (result.stack_price / result.stack_size
                            if result.stack_price is not None
                            else result.single_price)

            if single_price is None:
                continue

            total_gil += single_price * quantity

        total_profit = total_gil - simulation_cost
        return total_profit

    def _calculate_total_storage(self, results: dict[Result, int]) -> float:
        """
        Calculate the total character storage units required for all crafting results.

        Args:
            results (dict[Result, int]): Dictionary of Results and their quantities.

        Returns:
            float: The calculated total storage units required.
        """
        total_storage = 0
        store_item_threshold = SettingsManager.get_min_auction_list_price()

        for result, quantity in results.items():
            # If a stack price exists, use it in the calculation because stacks are more commonly sold
            # and it works as a low estimate
            single_price = (result.stack_price / result.stack_size
                            if result.stack_price is not None
                            else result.single_price)

            if single_price is None:
                continue

            # Add crafted items to storage if they are above the sell threshold
            if single_price * result.stack_size > store_item_threshold:
                total_storage += quantity / result.stack_size

        return total_storage
