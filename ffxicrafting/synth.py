import random
from collections import defaultdict
from ingredient import Ingredient
from config import Config
from table import Table
from controllers.item_controller import ItemController
from controllers.auction_controller import AuctionController
from utils import clamp


class Synth:
    SUCCESS_PROBABILITY = 0.95
    DESYNTH_SUCCESS_PROBABILITY = 0.45
    MIN_SUCCESS_PROBABILITY = 0.05
    MIN_HQ_PROBABILITY = 0.0006
    HQ_PROBABILITIES = [0.0006, 0.018, 0.0625, 0.25, 0.5]
    DESYNTH_HQ_PROBABILITIES = [0.37, 0.4, 0.43, 0.46, 0.49]
    HQ_TIER_WEIGHTS = [75, 18.75, 6.25]
    DESYNTH_HQ_TIER_WEIGHTS = [37.5, 37.5, 25]

    def __init__(self, recipe, crafter) -> None:
        self.recipe = recipe
        self.crafter = crafter
        self.difficulty = self.get_difficulty()
        self.can_craft = self.check_can_craft()
        self.tier = self.get_tier()
        self.num_trials = Config.get_simulation_trials()

    def get_result_names(self):
        return [ItemController.get_formatted_item_name(self.recipe.result),
                ItemController.get_formatted_item_name(self.recipe.result_hq1),
                ItemController.get_formatted_item_name(self.recipe.result_hq2),
                ItemController.get_formatted_item_name(self.recipe.result_hq3)]

    def get_result_quantities(self):
        return [self.recipe.result_qty,
                self.recipe.result_hq1_qty,
                self.recipe.result_hq2_qty,
                self.recipe.result_hq3_qty]

    def get_difficulty(self):
        recipe_skills = [self.recipe.wood, self.recipe.smith, self.recipe.gold,
                         self.recipe.cloth, self.recipe.leather,
                         self.recipe.bone, self.recipe.alchemy,
                         self.recipe.cook]

        crafter_skills = [self.crafter.skill_set.wood,
                          self.crafter.skill_set.smith,
                          self.crafter.skill_set.gold,
                          self.crafter.skill_set.cloth,
                          self.crafter.skill_set.leather,
                          self.crafter.skill_set.bone,
                          self.crafter.skill_set.alchemy,
                          self.crafter.skill_set.cook]

        skill_differences = [recipe - crafter for recipe, crafter in zip(recipe_skills, crafter_skills) if recipe > 0]
        return max(skill_differences, default=0)

    def get_tier(self):
        if self.difficulty < -50:
            return 3
        elif self.difficulty < -30:
            return 2
        elif self.difficulty < -10:
            return 1
        elif self.difficulty <= 0:
            return 0
        else:
            return -1

    def check_can_craft(self):
        skill_look_ahead = Config.get_skill_look_ahead()
        return self.difficulty - skill_look_ahead <= 0

    def attempt_success(self):
        success_probability = self.SUCCESS_PROBABILITY - \
            (self.difficulty / 10) if self.tier == -1 else self.SUCCESS_PROBABILITY
        if self.recipe.desynth:
            success_probability = self.DESYNTH_SUCCESS_PROBABILITY - \
                (self.difficulty / 10) if self.tier == -1 else self.DESYNTH_SUCCESS_PROBABILITY
        return random.random() < max(success_probability, self.MIN_SUCCESS_PROBABILITY)

    def attempt_hq(self):
        if self.recipe.desynth:
            hq_probability = self.DESYNTH_HQ_PROBABILITIES[self.tier + 1]
        else:
            hq_probability = self.HQ_PROBABILITIES[self.tier + 1]
        return random.random() < hq_probability

    def get_hq_tier(self):
        weights = self.DESYNTH_HQ_TIER_WEIGHTS if self.recipe.desynth else self.HQ_TIER_WEIGHTS
        return random.choices([1, 2, 3], weights=weights)[0]

    def synth(self):
        if self.attempt_success():
            if self.attempt_hq():
                hq_tier = self.get_hq_tier()
                return self.get_hq_result(hq_tier)
            return self.recipe.result, self.recipe.result_qty
        return None, None

    def get_hq_result(self, hq_tier):
        if hq_tier == 1:
            return self.recipe.result_hq1, self.recipe.result_hq1_qty
        elif hq_tier == 2:
            return self.recipe.result_hq2, self.recipe.result_hq2_qty
        else:
            return self.recipe.result_hq3, self.recipe.result_hq3_qty

    def do_synth_fail(self):
        loss_probability = clamp(0.15 - (self.difficulty / 20), 0, 1) if self.difficulty > 0 else 0.15
        if self.recipe.desynth:
            loss_probability += 0.35

        ingredient_ids = [i for i in [self.recipe.ingredient1, self.recipe.ingredient2, self.recipe.ingredient3,
                                      self.recipe.ingredient4, self.recipe.ingredient5, self.recipe.ingredient6,
                                      self.recipe.ingredient7, self.recipe.ingredient8] if i > 0]

        retained_ingredients = defaultdict(lambda: 0)
        for item_id in ingredient_ids:
            if random.random() >= loss_probability:
                retained_ingredients[item_id] += 1

        return retained_ingredients

    def simulate(self, num_times):
        results = defaultdict(lambda: 0)
        retained_ingredients = defaultdict(lambda: 0)

        for _ in range(num_times):
            item_id, quantity = self.synth()
            if item_id is not None:
                results[item_id] += quantity
            else:
                retained = self.do_synth_fail()
                for key, value in retained.items():
                    retained_ingredients[key] += value

        return results, retained_ingredients

    def calculate_cost(self):
        ingredient_ids = [i for i in [self.recipe.crystal, self.recipe.ingredient1, self.recipe.ingredient2,
                                      self.recipe.ingredient3, self.recipe.ingredient4, self.recipe.ingredient5,
                                      self.recipe.ingredient6, self.recipe.ingredient7, self.recipe.ingredient8] if i > 0]

        cost = 0
        for item_id in ingredient_ids:
            ingredient = Ingredient(item_id)
            if ingredient.price is None:
                return None
            cost += ingredient.price

        return round(cost, 2)

    def print_ingredient_costs(self):
        ingredient_ids = list(dict.fromkeys([i for i in [self.recipe.crystal, self.recipe.ingredient1, self.recipe.ingredient2,
                                                         self.recipe.ingredient3, self.recipe.ingredient4, self.recipe.ingredient5,
                                                         self.recipe.ingredient6, self.recipe.ingredient7, self.recipe.ingredient8] if i > 0]))

        column_labels = ["Ingredient", "Single", "Stack"]
        rows = []

        for id in ingredient_ids:
            ingredient = Ingredient(id)
            if ingredient.price is None:
                continue

            item = ItemController.get_item(id)
            item_name = item.sort_name.replace("_", " ").title()
            single_price = round(ingredient.price, 2)
            stack_price = round(ingredient.price * item.stack_size) if item.stack_size > 1 else ""

            rows.append([item_name, single_price, stack_price])

        table = Table(column_labels, rows)
        table.print()

    def calculate_stats(self):
        num_trials = Config.get_simulation_trials()
        results, retained_ingredients = self.simulate(num_trials)

        simulation_cost = self.cost * self.num_trials
        saved_cost = sum(Ingredient(ingredient_id).price * amount for ingredient_id,
                         amount in retained_ingredients.items())
        simulation_cost -= saved_cost

        total_storage = 0
        total_gil = 0

        for item_id, quantity in results.items():
            item = ItemController.get_item(item_id)
            auction_item = AuctionController.get_auction_item(item_id)

            if auction_item is None:
                continue

            single_price = auction_item.stack_price / item.stack_size if auction_item.stack_price > 0 else auction_item.single_price
            store_item_threshold = Config.get_store_item()

            if single_price * item.stack_size > store_item_threshold:
                total_storage += quantity / item.stack_size

            total_gil += single_price * quantity

        total_profit = total_gil - simulation_cost
        profit_per_synth = total_profit / self.num_trials
        profit_per_storage = total_profit / total_storage if total_storage > 0 else 0

        return round(profit_per_synth, 2), round(profit_per_storage, 2)
