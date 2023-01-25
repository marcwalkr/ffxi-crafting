import random
from collections import defaultdict
from ingredient import Ingredient
from config import Config
from auction_stats import AuctionStats
from controllers.item_controller import ItemController
from helpers import clamp


class Synth:
    def __init__(self, recipe, crafter) -> None:
        self.recipe = recipe
        self.crafter = crafter

        self.difficulty = self.get_difficulty()
        self.can_craft = self.can_craft()
        self.tier = self.get_tier()
        self.num_trials = Config.get_simulation_trials()

        self.cost = None
        self.profit_per_synth = None
        self.profit_per_inventory = None
        self.sell_frequency = None

    def get_result_names(self):
        nq_item = ItemController.get_item(self.recipe.result)
        nq_name = nq_item.sort_name.replace("_", " ").title()

        hq1_item = ItemController.get_item(self.recipe.result_hq1)
        hq1_name = hq1_item.sort_name.replace("_", " ").title()

        hq2_item = ItemController.get_item(self.recipe.result_hq2)
        hq2_name = hq2_item.sort_name.replace("_", " ").title()

        hq3_item = ItemController.get_item(self.recipe.result_hq3)
        hq3_name = hq3_item.sort_name.replace("_", " ").title()

        return nq_name, hq1_name, hq2_name, hq3_name

    def get_result_quantities(self):
        nq_quantity = self.recipe.result_qty
        hq1_quantity = self.recipe.result_hq1_qty
        hq2_quantity = self.recipe.result_hq2_qty
        hq3_quantity = self.recipe.result_hq3_qty

        return nq_quantity, hq1_quantity, hq2_quantity, hq3_quantity

    def get_difficulty(self):
        """Returns the largest skill difference between the recipe and the
        crafter of the required skills
        """
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

        skill_differences = []

        for (recipe, crafter) in zip(recipe_skills, crafter_skills):
            # The recipe doesn't require this craft
            if recipe == 0:
                continue

            skill_difference = recipe - crafter
            skill_differences.append(skill_difference)

        # The recipe difficulty is determined by the largest skill difference
        # of the required skills
        if len(skill_differences) > 0:
            return max(skill_differences)
        else:
            return 0

    def get_tier(self):
        """Returns the tier of the synth, which is determined by the skill
        difference between the recipe and the crafter and affects success and
        HQ rates"""
        if self.difficulty < -50:
            tier = 3
        elif self.difficulty < -30:
            tier = 2
        elif self.difficulty < -10:
            tier = 1
        elif self.difficulty <= 0:
            tier = 0
        else:
            tier = -1

        return tier

    def can_craft(self):
        """Returns True if the crafter is able to craft the recipe, taking into
        account the skill look ahead setting"""
        skill_look_ahead = Config.get_skill_look_ahead()
        enough_skill = self.difficulty - skill_look_ahead <= 0

        has_key_item = True
        if self.recipe.key_item > 0:
            has_key_item = self.recipe.key_item in self.crafter.key_items

        return enough_skill and has_key_item

    def attempt_success(self):
        """Used in a synth simulation, returns True if the synth was a
        success (not break)"""
        # Normal recipe, not desynth
        if not self.recipe.desynth:
            if self.tier == -1:
                success_probability = 0.95 - (self.difficulty / 10)
            else:
                success_probability = 0.95
        # Desynth recipe
        else:
            if self.tier == -1:
                success_probability = 0.45 - (self.difficulty / 10)
            else:
                success_probability = 0.45

        if success_probability < 0.05:
            success_probability = 0.05

        return random.random() < success_probability

    def attempt_hq(self):
        """Used in a synth simulation after success has been determined,
        returns True if the synth was HQ"""
        # Normal recipe, not desynth
        if not self.recipe.desynth:
            if self.tier == -1:
                hq_probability = 0.006
            elif self.tier == 0:
                hq_probability = 0.018
            elif self.tier == 1:
                hq_probability = 0.066
            elif self.tier == 2:
                hq_probability = 0.285
            else:
                hq_probability = 0.506
        # Desynth recipe
        else:
            if self.tier == -1:
                hq_probability = 0.37
            elif self.tier == 0:
                hq_probability = 0.4
            elif self.tier == 1:
                hq_probability = 0.43
            elif self.tier == 2:
                hq_probability = 0.46
            else:
                hq_probability = 0.49

        return random.random() < hq_probability

    def get_hq_tier(self):
        """Used in a synth simulation after HQ has been determined, returns
        which tier of HQ (1, 2, or 3)"""
        # Normal recipe, not desynth
        if not self.recipe.desynth:
            hq_tier = random.choices([1, 2, 3], weights=[75, 18.75, 6.25])
        # Desynth recipe
        else:
            hq_tier = random.choices([1, 2, 3], weights=[37.5, 37.5, 25])

        return hq_tier[0]

    def synth(self):
        """Simulates a single synth. Returns the item id of what was created
        and the quantity of the item, or (None, None) if the synth was a
        break"""
        success = self.attempt_success()
        if success:
            hq = self.attempt_hq()
            if hq:
                hq_tier = self.get_hq_tier()
                if hq_tier == 1:
                    item_id = self.recipe.result_hq1
                    quantity = self.recipe.result_hq1_qty
                elif hq_tier == 2:
                    item_id = self.recipe.result_hq2
                    quantity = self.recipe.result_hq2_qty
                else:
                    item_id = self.recipe.result_hq3
                    quantity = self.recipe.result_hq3_qty
            else:
                item_id = self.recipe.result
                quantity = self.recipe.result_qty

            return item_id, quantity
        else:
            return None, None

    def do_synth_fail(self):
        """Returns a dict of remaining ingredients and their quantities after a
        failed synth"""
        if self.difficulty > 0:
            loss_probability = clamp(0.15 - (self.difficulty / 20), 0, 1)
        else:
            loss_probability = 0.15

        if self.recipe.desynth:
            loss_probability += 0.35

        ingredient_ids = [self.recipe.ingredient1, self.recipe.ingredient2,
                          self.recipe.ingredient3, self.recipe.ingredient4,
                          self.recipe.ingredient5, self.recipe.ingredient6,
                          self.recipe.ingredient7, self.recipe.ingredient8]

        # Remove zeros (empty ingredient slots)
        ingredient_ids = [i for i in ingredient_ids if i > 0]

        retained_ingredients = defaultdict(lambda: 0)

        for item_id in ingredient_ids:
            if not random.random() < loss_probability:
                retained_ingredients[item_id] += 1

        return retained_ingredients

    def simulate(self, num_times):
        """Simulates the synth multiple times, the amount of times determined
        by the synth trials setting. Returns 2 dicts: the synth results and
        their quantities, and retained ingredients from failures and their
        quantities"""
        results = defaultdict(lambda: 0)
        retained_ingredients = defaultdict(lambda: 0)

        for _ in range(num_times):
            item_id, quantity = self.synth()
            if item_id is not None:
                results[item_id] += quantity
            else:
                # The synth failed, get list of retained ingredients
                retained = self.do_synth_fail()
                for key, value in retained.items():
                    retained_ingredients[key] += value

        return results, retained_ingredients

    def calculate_cost(self):
        """Returns the cost of a single synth"""
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

        return round(cost, 2)

    def calculate_stats(self):
        """Returns the average profit per synth, profit per inventory space,
        and sell frequency. The sell frequencies of each possible result are
        weighted by the probability of obtaining that result and added together
        for a single sell frequency"""
        # A dictionary containing all of the results from simulating the synth
        # several times
        # key: result item id, value: quantity
        num_trials = Config.get_simulation_trials()
        results, retained_ingredients = self.simulate(num_trials)

        # The total cost of every synth in the simulation
        simulation_cost = self.cost * self.num_trials

        # Subtract the price of remaining ingredients from the cost
        saved_cost = 0
        for ingredient_id, amount in retained_ingredients.items():
            ingredient = Ingredient(ingredient_id)
            saved_cost += ingredient.price * amount

        simulation_cost -= saved_cost

        total_inventory_space = 0
        total_gil = 0

        for item_id, quantity in results.items():
            item = ItemController.get_item(item_id)

            total_inventory_space += quantity / item.stack_size
            auction_stats = AuctionStats(item.name)

            if auction_stats.no_sales:
                continue

            if auction_stats.stack_price is not None:
                single_price = auction_stats.stack_price / item.stack_size
            else:
                single_price = auction_stats.single_price

            if single_price is None:
                single_price = 0

            gil = single_price * quantity

            total_gil += gil

        total_profit = total_gil - simulation_cost
        profit_per_synth = total_profit / self.num_trials
        profit_per_inventory = total_profit / total_inventory_space

        return round(profit_per_synth, 2), round(profit_per_inventory, 2)
