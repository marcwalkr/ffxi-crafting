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
        num_trials = SettingsManager.get_simulation_trials()
        self.set_ingredient_costs(item_controller)
        cost = self.recipe.calculate_cost()

        if not cost:
            # The synth cannot be crafted because of missing ingredients
            return None, None, None

        results, retained_ingredients = self.synth.simulate(num_trials)
        simulation_cost = self.calculate_simulation_cost(cost, num_trials, retained_ingredients)
        cost_per_item = self.calculate_cost_per_item(simulation_cost, results)
        total_profit, total_storage_slots = self.process_results(results, cost_per_item, item_controller)

        profit_per_synth = total_profit / num_trials
        profit_per_storage = total_profit / total_storage_slots if total_storage_slots > 0 else 0

        return results.keys(), profit_per_synth, profit_per_storage

    def set_ingredient_costs(self, item_controller):
        for ingredient in self.recipe.get_unique_ingredients():
            item_controller.update_vendor_cost(ingredient.item_id)
            item_controller.update_guild_cost(ingredient.item_id)
            item_controller.update_auction_data(ingredient.item_id)

    def calculate_simulation_cost(self, cost, num_trials, retained_ingredients):
        simulation_cost = cost * num_trials
        saved_cost = self.get_saved_cost(retained_ingredients)
        return simulation_cost - saved_cost

    def get_saved_cost(self, retained_ingredients):
        total_saved_cost = 0
        for ingredient, amount in retained_ingredients.items():
            min_cost = ingredient.get_min_cost()
            saved_cost = min_cost * amount
            total_saved_cost += saved_cost

        return total_saved_cost

    def calculate_cost_per_item(self, simulation_cost, results):
        total_items = sum(results.values())
        return simulation_cost / total_items if total_items > 0 else 0

    def process_results(self, results, cost_per_item, item_controller):
        total_profit = 0
        total_storage_slots = 0

        for result, quantity in results.items():
            item_controller.update_auction_data(result.item_id)

            self.calculate_result_profits(result, cost_per_item)

            total_profit += self.calculate_result_total_profit(result, quantity, cost_per_item)
            total_storage_slots += self.calculate_storage_slots(result, quantity)

        return total_profit, total_storage_slots

    def calculate_result_profits(self, result, cost_per_item):
        result.single_profit = result.single_price - cost_per_item if result.single_price is not None else None
        if result.stack_price is not None and result.stack_size > 1:
            result.stack_profit = result.stack_price - (cost_per_item * result.stack_size)
        else:
            result.stack_profit = None

    def calculate_result_total_profit(self, result, quantity, cost_per_item):
        # If a stack price exists, use it in the calculation
        # because stacks are more commonly sold and it works as a low estimate
        if result.stack_price is not None:
            single_price_from_stack = result.stack_price / result.stack_size
            return (single_price_from_stack - cost_per_item) * quantity
        elif result.single_price is not None:
            return (result.single_price - cost_per_item) * quantity
        else:
            return (0 - cost_per_item) * quantity

    def calculate_storage_slots(self, result, quantity):
        return (quantity + result.stack_size - 1) // result.stack_size
