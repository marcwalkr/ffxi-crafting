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
        recipe_skills = [
            (self.recipe.wood, self.crafter.wood),
            (self.recipe.smith, self.crafter.smith),
            (self.recipe.gold, self.crafter.gold),
            (self.recipe.cloth, self.crafter.cloth),
            (self.recipe.leather, self.crafter.leather),
            (self.recipe.bone, self.crafter.bone),
            (self.recipe.alchemy, self.crafter.alchemy),
            (self.recipe.cook, self.crafter.cook)
        ]

        max_required_skill = max((recipe for recipe, _ in recipe_skills if recipe > 0), default=0)
        if max_required_skill == 0:
            return 0

        corresponding_crafter_skill = next(crafter for recipe, crafter in recipe_skills if recipe == max_required_skill)

        return max_required_skill - corresponding_crafter_skill

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
            return self.recipe.get_nq_result()
        return None, None

    def get_hq_result(self, hq_tier):
        if hq_tier == 1:
            return self.recipe.get_hq_result(1)
        elif hq_tier == 2:
            return self.recipe.get_hq_result(2)
        else:
            return self.recipe.get_hq_result(3)

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

    def simulate(self, num_trials):

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

        return results, retained_ingredients
