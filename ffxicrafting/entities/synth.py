import random
from collections import defaultdict
from utils import clamp
from config import SettingsManager


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
        self.tier = self.get_tier()
        self.can_craft = self.check_can_craft()

    def check_can_craft(self):
        skill_look_ahead = SettingsManager.get_skill_look_ahead()
        return self.difficulty <= skill_look_ahead

    def get_difficulty(self):
        recipe_skills = [self.recipe.wood, self.recipe.smith, self.recipe.gold,
                         self.recipe.cloth, self.recipe.leather,
                         self.recipe.bone, self.recipe.alchemy,
                         self.recipe.cook]

        crafter_skills = [self.crafter.wood,
                          self.crafter.smith,
                          self.crafter.gold,
                          self.crafter.cloth,
                          self.crafter.leather,
                          self.crafter.bone,
                          self.crafter.alchemy,
                          self.crafter.cook]

        skill_differences = [recipe - crafter for recipe, crafter in zip(recipe_skills, crafter_skills)]
        return min(skill_differences, default=0)

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

        ingredients = self.recipe.get_ingredients()[1:]  # Remove the crystal

        retained_ingredients = defaultdict(lambda: 0)
        for ingredient in ingredients:
            if random.random() >= loss_probability:
                retained_ingredients[ingredient] += 1

        return retained_ingredients

    def calculate_cost(self, item_controller):
        self.set_ingredients_cost(item_controller)
        total_cost = 0
        for ingredient in self.recipe.get_ingredients():
            min_cost = ingredient.get_min_cost()
            if min_cost is None:
                return None
            total_cost += min_cost
        return total_cost

    def set_ingredients_cost(self, item_controller):
        for ingredient in self.recipe.get_unique_ingredients():
            item_controller.update_vendor_cost(ingredient.item_id)
            item_controller.update_guild_cost(ingredient.item_id)
            item_controller.update_auction_data(ingredient.item_id)

    def simulate(self, num_trials, item_controller):
        self.cost = self.calculate_cost(item_controller)
        if not self.cost:
            return None, None

        results = defaultdict(lambda: 0)
        retained_ingredients = defaultdict(lambda: 0)

        for _ in range(num_trials):
            result, quantity = self.synth()
            if result is not None:
                results[result] += quantity
            else:
                retained = self.do_synth_fail()
                for result_retained, quantity_retained in retained.items():
                    retained_ingredients[result_retained] += quantity_retained

        simulation_cost = self.cost * num_trials

        # Subtract the total cost saved from retained ingredients after failures
        simulation_cost -= self.get_saved_cost(retained_ingredients)

        return simulation_cost, results

    def get_saved_cost(self, retained_ingredients):
        total_saved_cost = 0
        for ingredient, amount in retained_ingredients.items():
            min_cost = ingredient.get_min_cost()
            saved_cost = min_cost * amount
            total_saved_cost += saved_cost

        return total_saved_cost
