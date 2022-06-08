from database import Database
from helpers import older_than
from config import Config
from models.item import Item
from models.item_cost import ItemCost
from controllers.auction_controller import AuctionController
from controllers.vendor_controller import VendorController
from controllers.guild_controller import GuildController


class ItemController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_item(cls, item_id):
        item_tuple = cls.db.get_item(item_id)

        if item_tuple is not None:
            return Item(*item_tuple)
        else:
            return None

    @classmethod
    def get_item_cost(cls, item_id):
        item_cost_tuple = cls.db.get_item_cost(item_id)

        if item_cost_tuple is not None:
            item_cost = ItemCost(*item_cost_tuple)

            if cls.outdated_cost(item_cost):
                cls.search_update_item_cost(item_id)
        else:
            cls.search_add_item_cost(item_id)
            item_cost = cls.get_item_cost(item_id)

        return item_cost

    @classmethod
    def add_item_cost(cls, item_id, source_id, cost):
        cls.db.add_item_cost(item_id, source_id, cost)

    @classmethod
    def update_item_cost(cls, item_id, source_id, cost):
        cls.db.update_item_cost(item_id, source_id, cost)

    @classmethod
    def search_add_item_cost(cls, item_id):
        source_id, cost = cls.search_cheapest_price(item_id)
        cls.add_item_cost(item_id, source_id, cost)

    @classmethod
    def search_update_item_cost(cls, item_id):
        source_id, cost = cls.search_cheapest_price(item_id)
        cls.update_item_cost(item_id, source_id, cost)

    @classmethod
    def search_cheapest_price(cls, item_id):
        auction_price = cls.get_auction_price(item_id)
        vendor_id, vendor_price = cls.get_vendor_price(item_id)
        guild_id, guild_price = cls.get_guild_price(item_id)

        ignore_guilds = Config.get_ignore_guilds()
        if ignore_guilds:
            sources = [0, vendor_id]
            prices = [auction_price, vendor_price]
        else:
            sources = [0, vendor_id, guild_id]
            prices = [auction_price, vendor_price, guild_price]

        cheapest_price = min(prices)
        index = prices.index(cheapest_price)
        source_id = sources[index]

        # Use max price value and NULL source for items that couldn't be found
        if cheapest_price == 999999999:
            source_id = None

        return source_id, cheapest_price

    @classmethod
    def get_auction_price(cls, item_id):
        auction = AuctionController.get_auction(item_id)

        prices = []

        if auction.single_price is not None:
            prices.append(auction.single_price)

        if auction.stack_price is not None:
            # Get the item for the stack size
            item = cls.get_item(item_id)

            single_price_from_stack = auction.stack_price / item.stack_size
            prices.append(single_price_from_stack)

        if len(prices) > 0:
            return min(prices)
        else:
            return 999999999

    @staticmethod
    def get_vendor_price(item_id):
        vendor_items = VendorController.get_vendor_items(item_id)

        npc_ids = []
        prices = []

        for vendor_item in vendor_items:
            npc_ids.append(vendor_item.npc_id)
            prices.append(vendor_item.price)

        if len(prices) > 0:
            # Get the cheapest price and the id for the NPC that sells it
            min_price = min(prices)
            index = prices.index(min_price)
            npc_id = npc_ids[index]

            return npc_id, min_price
        else:
            return None, 999999999

    @staticmethod
    def get_guild_price(item_id):
        guild_shops = GuildController.get_guild_shops(item_id)

        guild_ids = []
        prices = []

        for guild_shop in guild_shops:
            # Make sure the guild regularly stocks the item
            if guild_shop.initial_quantity > 0:
                guild_ids.append(guild_shop.guild_id)
                prices.append(guild_shop.min_price)

        if len(prices) > 0:
            # Get the cheapest price and the id for the guild that sells it
            min_price = min(prices)
            index = prices.index(min_price)
            guild_id = guild_ids[index]

            return guild_id, min_price
        else:
            return None, 999999999

    @staticmethod
    def outdated_cost(item_cost):
        """Return True if the item cost data is older than 7 days"""
        return older_than(item_cost.last_updated, 7)
