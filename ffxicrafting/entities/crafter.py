from ..config import SettingsManager
from .synth import Synth


class Crafter:
    def __init__(self, wood, smith, gold, cloth, leather, bone, alchemy, cook, recipe) -> None:
        self.wood = wood
        self.smith = smith
        self.gold = gold
        self.cloth = cloth
        self.leather = leather
        self.bone = bone
        self.alchemy = alchemy
        self.cook = cook
        self.recipe = recipe
        self.synth = Synth(recipe, self)

    def craft(self, num_times):
        results, retained_ingredients = self.synth.simulate(num_times)

        # Calculate the total cost saved from retained ingredients after failures
        simulation_cost = self.synth.cost * num_times
        for ingredient_id, amount in retained_ingredients.items():
            ingredient = None
            for item in self.recipe.get_ingredients():
                if item.item_id == ingredient_id:
                    ingredient = item
                    break
            saved_cost = ingredient.min_price * amount
            simulation_cost -= saved_cost

        total_storage = 0
        total_gil = 0

        for item_id, quantity in results.items():
            result = None
            for item in self.recipe.get_results():
                if item.item_id == item_id:
                    result = item
                    break

            single_price = (result.stack_price / result.stack_size
                            if result.stack_price not in (None, 0)
                            else result.single_price)

            if single_price in (None, 0):
                continue

            store_item_threshold = SettingsManager.get_min_sell_price()

            # Add crafted items to storage if they are above the sell threshold
            if single_price * result.stack_size > store_item_threshold:
                total_storage += quantity / result.stack_size

            total_gil += single_price * quantity

        total_profit = total_gil - simulation_cost
        profit_per_synth = total_profit / num_times
        profit_per_storage = total_profit / total_storage if total_storage > 0 else 0

        return int(profit_per_synth), int(profit_per_storage)
