from entities import Item
from database import Database
from config import SettingsManager
from controllers import AuctionController, VendorController, GuildController


class ItemService:
    db = Database()
    item_cache = {}

    @classmethod
    def get_item(cls, item_id):
        if item_id in cls.item_cache:
            return cls.item_cache[item_id]

        item_tuple = cls.db.get_item(item_id)
        if item_tuple is not None:
            item = Item(*item_tuple)
            cls.item_cache[item_id] = item
            return item
        else:
            return None

    @classmethod
    def get_items(cls, item_ids):
        items = []
        for item_id in item_ids:
            item = cls.get_item(item_id)
            if item is not None:
                items.append(item)
        return items

    @classmethod
    def update_auction_data(cls, item_id):
        item = cls.get_item(item_id)
        if item.single_price is None or item.stack_price is None or item.single_sell_freq is None or item.stack_sell_freq is None:
            auction_data = cls.get_auction_data(item_id)
            single_price, stack_price, single_sell_freq, stack_sell_freq = auction_data

            if item.stack_size > 1 and stack_price is not None:
                single_price_from_stack = int(stack_price / item.stack_size)
            else:
                single_price_from_stack = None

            item.single_price = int(single_price) if single_price is not None else 0
            item.stack_price = int(stack_price) if stack_price is not None else 0
            item.single_sell_freq = float(f"{single_sell_freq:.4f}") if single_sell_freq is not None else 0
            item.stack_sell_freq = float(f"{stack_sell_freq:.4f}") if stack_sell_freq is not None else 0

            # Determine the minimum auction price, ignoring 0 values
            prices_to_check = [item.single_price, single_price_from_stack]
            min_auction_price = min((price for price in prices_to_check if price not in (None, 0)), default=None)

            # Update min_price if the new min_auction_price is lower
            if min_auction_price is not None and (item.min_price is None or min_auction_price < item.min_price):
                item.min_price = min_auction_price

    @classmethod
    def update_vendor_data(cls, item_id):
        item = cls.get_item(item_id)
        item.min_vendor_price = cls.get_vendor_price(item_id)

        # Update min_price if the min_vendor_price is lower
        if item.min_vendor_price is not None and (item.min_price is None or item.min_vendor_price < item.min_price):
            item.min_price = item.min_vendor_price

    @classmethod
    def get_auction_data(cls, item_id):
        # Set crystals to 100 gil to test profit table
        if item_id >= 4096 and item_id <= 4103:
            return 100, None, 50, None
        auction_item = AuctionController.get_auction_item(item_id, is_stack=False)
        stack_auction_item = AuctionController.get_auction_item(item_id, is_stack=True)
        if auction_item is None or auction_item.avg_price <= 0:
            single_price = None
            single_sell_freq = None
        else:
            single_price = auction_item.avg_price
            single_sell_freq = auction_item.sell_freq

        if stack_auction_item is None or stack_auction_item.avg_price <= 0:
            stack_price = None
            stack_sell_freq = None
        else:
            stack_price = stack_auction_item.avg_price
            stack_sell_freq = stack_auction_item.sell_freq

        return single_price, stack_price, single_sell_freq, stack_sell_freq

    @classmethod
    def get_vendor_price(cls, item_id):
        vendor_items = VendorController.get_vendor_items(item_id)
        regional_vendors = VendorController.get_regional_vendors()
        enabled_regional_merchants = SettingsManager.get_enabled_regional_merchants()

        filtered_vendor_items = []
        regional_vendor_ids = {vendor.npc_id: vendor.region for vendor in regional_vendors}

        for vendor_item in vendor_items:
            vendor_region = regional_vendor_ids.get(vendor_item.npc_id)
            if vendor_region is None or vendor_region in enabled_regional_merchants:
                filtered_vendor_items.append(vendor_item)

        prices = [vendor_item.price for vendor_item in filtered_vendor_items]

        guild_price = cls.get_guild_price(item_id)
        if guild_price is not None:
            prices.append(guild_price)

        return min(prices, default=None)

    @classmethod
    def get_guild_price(cls, item_id):
        enabled_guilds = SettingsManager.get_enabled_guilds()
        guild_shops = GuildController.get_guild_shops(item_id)
        prices = []

        for shop in guild_shops:
            if shop.initial_quantity > 0:
                guild = GuildController.get_guild(shop.guild_id)
                if guild and guild.category in enabled_guilds:
                    prices.append(shop.min_price)

        return min(prices, default=None)
