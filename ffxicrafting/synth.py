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
        if self.cost is None:
            return None, None

        # The total cost is the cost of a single synth * the number of times
        # the synth will be simulated
        total_cost = self.cost * self.num_trials

        # A dictionary containing all of the results from simulating the synth
        # several times
        # key: result item id, value: quantity
        results = self.simulate()

        # The total number of items that were produced in the simulation
        num_items = sum(results.values())

        gil_sum = 0
        overall_frequency = 0

        # Loop through each result item in the dictionary
        for item_id, quantity in results.items():
            item = ItemController.get_item(item_id)
            auction_stats = AuctionController.get_auction_stats(item_id)

            # The item either can't be sold or was never sold on the AH
            if (auction_stats.average_single_price is None and
                    auction_stats.average_stack_price is None):
                continue

            # Use the sell price and frequency of whichever form of the item
            # sells faster: single or stack, prioritizing stack if they sell
            # equally fast
            if (auction_stats.stack_sells_faster or
                    auction_stats.single_stack_equal_frequency):
                single_cost = auction_stats.average_stack_price / item.stack_size
                frequency = auction_stats.average_stack_frequency
            else:
                single_cost = auction_stats.average_single_price
                frequency = auction_stats.average_single_frequency

            gil_sum += single_cost * quantity

            # The weight is the proportion of the results that this item takes
            # up, e.g. 0.5 if this result is exactly half of the results
            weight = quantity / num_items

            # Multiply this result's sell frequency by its weight. This
            # determines how this result's sell frequency affects the overall
            # frequency calculation. If the result is very uncommon, e.g. HQ3
            # only, then it will only affect the overall frequency a small
            # amount.
            weighted_frequency = frequency * weight

            # Add all of the weighted frequencies together to determine the
            # overall sell frequency
            overall_frequency += weighted_frequency

        average_profit = (gil_sum - total_cost) / self.num_trials

        return round(average_profit, 2), round(overall_frequency, 2)
