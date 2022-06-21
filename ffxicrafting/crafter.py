from config import Config
from controllers.auction_controller import AuctionController
from controllers.guild_controller import GuildController
from controllers.vendor_controller import VendorController
from controllers.item_controller import ItemController


class Crafter:
    def __init__(self, skill_set, key_items=[]) -> None:
        self.skill_set = skill_set
        self.key_items = key_items

    def get_outcome_chances(self, recipe):
        tier = self.get_tier(recipe)

        # Normal recipe, not desynth
        if recipe.desynth != 1:
            # After HQ has been decided, the chances for each tier
            hq1_chance = 0.75
            hq2_chance = 0.1875
            hq3_chance = 0.0625

            if tier == -1:
                skill_diff = self.get_skill_difference(recipe)
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
                skill_diff = self.get_skill_difference(recipe)
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

        nq = success_rate * (1 - hq_chance)
        hq1 = success_rate * hq_chance * hq1_chance
        hq2 = success_rate * hq_chance * hq2_chance
        hq3 = success_rate * hq_chance * hq3_chance

        return nq, hq1, hq2, hq3

    def get_tier(self, recipe):
        diff = self.get_skill_difference(recipe)

        if diff > 50:
            tier = 3
        elif diff > 30:
            tier = 2
        elif diff > 10:
            tier = 1
        elif diff >= 0:
            tier = 0
        else:
            tier = -1

        return tier

    def get_skill_difference(self, recipe):
        recipe_skills = [recipe.wood, recipe.smith, recipe.gold, recipe.cloth,
                         recipe.leather, recipe.bone, recipe.alchemy,
                         recipe.cook]

        my_skills = [self.skill_set.wood, self.skill_set.smith,
                     self.skill_set.gold, self.skill_set.cloth,
                     self.skill_set.leather, self.skill_set.bone,
                     self.skill_set.alchemy, self.skill_set.cook]

        diffs = []

        for i in range(len(recipe_skills)):
            recipe_skill = recipe_skills[i]

            # The recipe doesn't require this craft
            if recipe_skill == 0:
                continue

            my_skill = my_skills[i]
            diff = my_skill - recipe_skill
            diffs.append(diff)

        # The lowest skill difference determines recipe difficulty
        return min(diffs)

    @classmethod
    def search_cheapest_price(cls, item_id):
        auction_price = cls.get_auction_price(item_id)
        vendor_price = cls.get_vendor_price(item_id)
        guild_price = cls.get_guild_price(item_id)

        ignore_guilds = Config.get_ignore_guilds()
        if ignore_guilds:
            prices = [auction_price, vendor_price]
        else:
            prices = [auction_price, vendor_price, guild_price]

        return min(prices)

    @staticmethod
    def get_auction_price(item_id):
        auction = AuctionController.get_auction(item_id)

        prices = []

        if auction.single_price is not None:
            prices.append(auction.single_price)

        if auction.stack_price is not None:
            # Get the item for the stack size
            item = ItemController.get_item(item_id)

            single_price_from_stack = auction.stack_price / item.stack_size
            prices.append(single_price_from_stack)

        if len(prices) > 0:
            return min(prices)
        else:
            return 999999999

    @staticmethod
    def get_vendor_price(item_id):
        vendor_items = VendorController.get_vendor_items(item_id)

        prices = []

        for vendor_item in vendor_items:
            prices.append(vendor_item.price)

        if len(prices) > 0:
            return min(prices)
        else:
            return 999999999

    @staticmethod
    def get_guild_price(item_id):
        guild_shops = GuildController.get_guild_shops(item_id)

        prices = []

        for guild_shop in guild_shops:
            # Make sure the guild regularly stocks the item
            if guild_shop.initial_quantity > 0:
                prices.append(guild_shop.min_price)

        if len(prices) > 0:
            return min(prices)
        else:
            return 999999999

    @classmethod
    def calculate_synth_cost(cls, recipe):
        ingredient_ids = [recipe.crystal, recipe.ingredient1,
                          recipe.ingredient2, recipe.ingredient3,
                          recipe.ingredient4, recipe.ingredient5,
                          recipe.ingredient6, recipe.ingredient7,
                          recipe.ingredient8]

        # Remove zeros (empty ingredient slots)
        ingredient_ids = [i for i in ingredient_ids if i > 0]

        cost = 0
        for id in ingredient_ids:
            item_cost = cls.search_cheapest_price(id)
            cost += item_cost

        return cost
