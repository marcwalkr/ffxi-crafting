from controllers.auction_controller import AuctionController
from controllers.item_controller import ItemController
from controllers.vendor_controller import VendorController
from controllers.guild_controller import GuildController
from config import Config


class Ingredient:
    def __init__(self, item_id) -> None:
        self.item_id = item_id
        self.price = self.get_cheapest_price()

    def get_cheapest_price(self):
        auction_price = self.get_auction_price()
        vendor_price = self.get_vendor_price()
        guild_price = self.get_guild_price()

        ignore_guilds = Config.get_ignore_guilds()

        prices = []

        if auction_price is not None:
            prices.append(auction_price)

        if vendor_price is not None:
            prices.append(vendor_price)

        if not ignore_guilds and guild_price is not None:
            prices.append(guild_price)

        if len(prices) > 0:
            return min(prices)
        else:
            return None

    def get_auction_price(self):
        auction_stats = AuctionController.get_auction_stats(self.item_id)

        prices = []

        if auction_stats.average_single_price is not None:
            prices.append(auction_stats.average_single_price)

        if auction_stats.average_stack_price is not None:
            # Get the item for the stack size
            item = ItemController.get_item(self.item_id)

            single_price_from_stack = (auction_stats.average_stack_price /
                                       item.stack_size)
            prices.append(single_price_from_stack)

        if len(prices) > 0:
            return min(prices)
        else:
            return None

    def get_vendor_price(self):
        vendor_items = VendorController.get_vendor_items(self.item_id)

        prices = []

        for vendor_item in vendor_items:
            prices.append(vendor_item.price)

        if len(prices) > 0:
            return min(prices)
        else:
            return None

    def get_guild_price(self):
        guild_shops = GuildController.get_guild_shops(self.item_id)

        prices = []

        for guild_shop in guild_shops:
            # Make sure the guild regularly stocks the item
            if guild_shop.initial_quantity > 0:
                prices.append(guild_shop.min_price)

        if len(prices) > 0:
            return min(prices)
        else:
            return None
