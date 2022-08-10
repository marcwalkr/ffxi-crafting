from ingredient import Ingredient


class Synth:
    def __init__(self, recipe, crafter) -> None:
        self.recipe = recipe
        self.crafter = crafter

        self.skill_difference = self.get_skill_difference()

        outcome_chances = self.get_outcome_chances()
        self.expected_nq_qty = self.recipe.result_qty * outcome_chances[0]
        self.expected_hq1_qty = self.recipe.result_hq1_qty * outcome_chances[1]
        self.expected_hq2_qty = self.recipe.result_hq2_qty * outcome_chances[2]
        self.expected_hq3_qty = self.recipe.result_hq3_qty * outcome_chances[3]

    def get_outcome_chances(self):
        tier = self.get_tier()

        # Normal recipe, not desynth
        if self.recipe.desynth != 1:
            # After HQ has been decided, the chances for each tier
            hq1_chance = 0.75
            hq2_chance = 0.1875
            hq3_chance = 0.0625

            if tier == -1:
                skill_diff = self.get_skill_difference()
                success_rate = 0.95 - (skill_diff / 10)
                hq_chance = 0.0006

            elif tier == 0:
                success_rate = 0.95
                hq_chance = 0.018

            elif tier == 1:
                success_rate = 0.95
                hq_chance = 0.066

            elif tier == 2:
                success_rate = 0.95
                hq_chance = 0.285

            elif tier == 3:
                success_rate = 0.95
                hq_chance = 0.506

        # Desynth recipe
        else:
            # After HQ has been decided, the chances for each tier
            hq1_chance = 0.375
            hq2_chance = 0.375
            hq3_chance = 0.25

            if tier == -1:
                skill_diff = self.get_skill_difference()
                success_rate = 0.45 - (skill_diff / 10)
                hq_chance = 0.37

            elif tier == 0:
                success_rate = 0.45
                hq_chance = 0.4

            elif tier == 1:
                success_rate = 0.45
                hq_chance = 0.43

            elif tier == 2:
                success_rate = 0.45
                hq_chance = 0.46

            elif tier == 3:
                success_rate = 0.45
                hq_chance = 0.49

        if success_rate < 0.05:
            success_rate = 0.05

        nq = success_rate * (1 - hq_chance)
        hq1 = success_rate * hq_chance * hq1_chance
        hq2 = success_rate * hq_chance * hq2_chance
        hq3 = success_rate * hq_chance * hq3_chance

        return nq, hq1, hq2, hq3

    def get_tier(self):
        diff = self.get_skill_difference()

        if diff < -50:
            tier = 3
        elif diff < -30:
            tier = 2
        elif diff < -10:
            tier = 1
        elif diff <= 0:
            tier = 0
        else:
            tier = -1

        return tier

    def get_skill_difference(self):
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

        diffs = []

        for i in range(len(recipe_skills)):
            recipe_skill = recipe_skills[i]

            # The recipe doesn't require this craft
            if recipe_skill == 0:
                continue

            crafter_skill = crafter_skills[i]
            diff = recipe_skill - crafter_skill
            diffs.append(diff)

        # The max skill difference determines recipe difficulty
        if len(diffs) > 0:
            return max(diffs)
        else:
            return 100

    def calculate_cost(self):
        ingredient_ids = [self.recipe.crystal, self.recipe.ingredient1,
                          self.recipe.ingredient2, self.recipe.ingredient3,
                          self.recipe.ingredient4, self.recipe.ingredient5,
                          self.recipe.ingredient6, self.recipe.ingredient7,
                          self.recipe.ingredient8]

        # Remove zeros (empty ingredient slots)
        ingredient_ids = [i for i in ingredient_ids if i > 0]

        cost = 0
        for item_id in ingredient_ids:
            ingredient = Ingredient(item_id)

            if ingredient.price is None:
                return None

            cost += ingredient.price

        return cost
