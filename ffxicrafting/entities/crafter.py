from entities import Synth
from config import SettingsManager


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

    def craft(self, item_controller):
        num_trials = SettingsManager.get_simulation_trials()
        simulation_cost, results = self.synth.simulate(num_trials, item_controller)

        if not simulation_cost or not results:
            return [], None, None

        # Calculate and set the expected profit for each result, selling them as singles and stacks
        self._set_results_profit(results, simulation_cost, item_controller)

        # Calculate the overall expected profit per synth and per character storage unit
        profit_per_synth = self._get_profit_per_synth(results, simulation_cost, num_trials)
        profit_per_storage = self._get_profit_per_storage(results, simulation_cost)

        return results.keys(), int(profit_per_synth), int(profit_per_storage)

    def _set_results_profit(self, results, simulation_cost, item_controller):
        for result, quantity in results.items():
            item_controller.update_auction_data(result.item_id)
            result.single_profit = self._get_single_profit(result, quantity, simulation_cost)
            result.stack_profit = self._get_stack_profit(result, quantity, simulation_cost)

    def _get_single_profit(self, result, quantity, simulation_cost):
        return self._calculate_profit(result, quantity, simulation_cost, "single_price", "stack_size", single=True)

    def _get_stack_profit(self, result, quantity, simulation_cost):
        return self._calculate_profit(result, quantity, simulation_cost, "stack_price", "stack_size", single=False)

    def _calculate_profit(self, result, quantity, simulation_cost, price_attr, stack_size_attr, single=True):
        price = getattr(result, price_attr)
        stack_size = getattr(result, stack_size_attr)
        if price is None or (not single and stack_size == 1):
            return None
        cost_per_item = simulation_cost / quantity
        if single:
            profit = price - cost_per_item
        else:
            profit = price - cost_per_item * stack_size
        return int(profit)

    def _get_profit_per_synth(self, results, simulation_cost, num_trials):
        total_profit = self._calculate_total_profit(results, simulation_cost)
        profit_per_synth = total_profit / num_trials
        return profit_per_synth

    def _get_profit_per_storage(self, results, simulation_cost):
        total_profit = self._calculate_total_profit(results, simulation_cost)
        total_storage = self._calculate_total_storage(results)
        profit_per_storage = total_profit / total_storage if total_storage > 0 else 0
        return profit_per_storage

    def _calculate_total_profit(self, results, simulation_cost):
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

    def _calculate_total_storage(self, results):
        total_storage = 0
        store_item_threshold = SettingsManager.get_min_sell_price()

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
