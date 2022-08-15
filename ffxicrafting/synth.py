import random
from collections import defaultdict
from ingredient import Ingredient
from config import Config
from controllers.item_controller import ItemController
from controllers.auction_controller import AuctionController


class Synth:
    def __init__(self, recipe, crafter) -> None:
        self.recipe = recipe
        self.crafter = crafter

        self.difficulty = self.get_difficulty()
        self.tier = self.get_tier()
        self.can_craft = self.can_craft()
        self.num_trials = Config.get_synth_trials()

        self.cost = None
        self.profit = None
        self.sell_frequency = None

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
        """Returns True if the crafter is able to craft the recipe, determined
        by if their skill is high enough, taking into account the skill look
        ahead setting, and if the crafter has any required key item"""
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

    def simulate(self):
        """Simulates the synth multiple times, the amount of times determined
        by the synth trials setting. Returns a dictionary containing all of the
        results and their quantities"""
        results = defaultdict(lambda: 0)

        for _ in range(self.num_trials):
            item_id, quantity = self.synth()
            if item_id is not None:
                results[item_id] += quantity

        return results

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

    def calculate_profit_and_frequency(self):
        """Returns the average profit and sell frequency of a single synth. The
        sell frequencies of each possible result are weighted by the
        probability of obtaining that result and added together to obtain a
        single sell frequency"""
        # A dictionary containing all of the results from simulating the synth
        # several times
        # key: result item id, value: quantity
        results = self.simulate()

        # The total cost of every synth in the simulation
        simulation_cost = self.cost * self.num_trials

        # The total number of items that were produced in the simulation
        simulation_num_items = sum(results.values())

        gil_sum = 0
        overall_frequency = 0

        for item_id, quantity in results.items():
            item = ItemController.get_item(item_id)
            auction_stats = AuctionController.get_auction_stats(item_id)

            if auction_stats.no_sales:
                continue

            if auction_stats.stack_sells_faster:
                single_price = (auction_stats.average_stack_price /
                                item.stack_size)
                frequency = auction_stats.average_stack_frequency
            else:
                single_price = auction_stats.average_single_price
                frequency = auction_stats.average_single_frequency

            gil = single_price * quantity

            # The weight is the proportion of the results that is this item
            weight = quantity / simulation_num_items

            # The frequency is weighted so it affects the overall frequency
            # more the more commonly the result item is obtained from the synth
            weighted_frequency = frequency * weight

            gil_sum += gil
            overall_frequency += weighted_frequency

        average_profit = (gil_sum - simulation_cost) / self.num_trials

        return round(average_profit, 2), round(overall_frequency, 2)
