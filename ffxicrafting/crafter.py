from config import Config
from controllers.auction_controller import AuctionController
from controllers.guild_controller import GuildController
from controllers.vendor_controller import VendorController
from controllers.item_controller import ItemController


class Crafter:
    def __init__(self, skill_set, key_items=[]) -> None:
        self.skill_set = skill_set
        self.key_items = key_items

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
