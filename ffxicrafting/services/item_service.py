from entities import Item
from config import SettingsManager
from controllers import AuctionController, VendorController, GuildController


class ItemService:
    _cache = {}

    def __init__(self, db) -> None:
        self.db = db
        self.auction_controller = AuctionController(db)
        self.vendor_controller = VendorController(db)
        self.guild_controller = GuildController(db)

    def get_items(self, item_ids):
        # Identify the missing item_ids (those not in the cache)
        missing_item_ids = [item_id for item_id in item_ids if item_id not in self._cache]

        # Query the database only for the missing items
        if missing_item_ids:
            item_tuples = self.db.get_items(missing_item_ids)
            if item_tuples:
                for item_tuple in item_tuples:
                    item = Item(*item_tuple)
                    self._cache[item.id] = item

        # Retrieve all items from the cache
        items = [self._cache[item_id] for item_id in item_ids if item_id in self._cache]
        return items

    def get_item(self, item_id):
        if item_id in self._cache:
            return self._cache[item_id]
        else:
            raise ValueError(f"Item with id {item_id} not found in cache.")

    def update_auction_data(self, item_id):
        item = self.get_item(item_id)
        if item.single_price is None or item.stack_price is None or item.single_sell_freq is None or item.stack_sell_freq is None:
            auction_data = self.get_auction_data(item_id)
            single_price, stack_price, single_sell_freq, stack_sell_freq = auction_data

            item.single_price = int(single_price) if single_price is not None else None
            item.stack_price = int(stack_price) if stack_price is not None else None
            item.single_sell_freq = float(f"{single_sell_freq:.4f}") if single_sell_freq is not None else None
            item.stack_sell_freq = float(f"{stack_sell_freq:.4f}") if stack_sell_freq is not None else None

            self.update_min_price(item_id)

    def update_vendor_data(self, item_id):
        item = self.get_item(item_id)
        item.min_vendor_price = self.get_vendor_price(item_id)
        self.update_min_price(item_id)

    def update_min_price(self, item_id):
        item = self.get_item(item_id)
        min_vendor_price = self.get_vendor_price(item_id)

        single_price, stack_price, _, _ = self.get_auction_data(item_id)

        if item.stack_size > 1 and stack_price is not None:
            single_price_from_stack = int(stack_price / item.stack_size)
        else:
            single_price_from_stack = None

        # Determine the minimum auction price and filter out None values
        min_auction_price = min(
            (price for price in [single_price, single_price_from_stack] if price is not None),
            default=None
        )

        # Determine the minimum price considering vendor and auction prices
        item.min_price = min(
            (price for price in [min_vendor_price, min_auction_price] if price is not None),
            default=None
        )

    def get_auction_data(self, item_id):
        # Set single crystal prices to 100 gil to test profit table
        if item_id >= 4096 and item_id <= 4103:
            return 100, None, 50, None

        auction_items = self.auction_controller.get_auction_items(item_id)
        single_price = None
        stack_price = None
        single_sell_freq = None
        stack_sell_freq = None

        for auction_item in auction_items:
            if not auction_item.is_stack:
                single_price = auction_item.avg_price if auction_item.avg_price > 0 else None
                single_sell_freq = auction_item.sell_freq if auction_item.sell_freq > 0 else None
            else:
                stack_price = auction_item.avg_price if auction_item.avg_price > 0 else None
                stack_sell_freq = auction_item.sell_freq if auction_item.sell_freq > 0 else None

        return single_price, stack_price, single_sell_freq, stack_sell_freq

    def get_vendor_price(self, item_id):
        vendor_items = self.vendor_controller.get_vendor_items(item_id)
        regional_vendors = self.vendor_controller.get_regional_vendors()
        enabled_regional_merchants = SettingsManager.get_enabled_regional_merchants()

        filtered_vendor_items = []
        regional_vendor_ids = {vendor.npc_id: vendor.region for vendor in regional_vendors}

        for vendor_item in vendor_items:
            vendor_region = regional_vendor_ids.get(vendor_item.npc_id)
            if vendor_region is None or vendor_region in enabled_regional_merchants:
                filtered_vendor_items.append(vendor_item)

        prices = [vendor_item.price for vendor_item in filtered_vendor_items]

        guild_price = self.get_guild_price(item_id)
        if guild_price is not None:
            prices.append(guild_price)

        return min(prices, default=None)

    def get_guild_price(self, item_id):
        enabled_guilds = SettingsManager.get_enabled_guilds()
        guild_shops = self.guild_controller.get_guild_shops(item_id)
        prices = []

        for shop in guild_shops:
            if shop.initial_quantity > 0:
                guild = self.guild_controller.get_guild(shop.guild_id)
                if guild and guild.category in enabled_guilds:
                    prices.append(shop.min_price)

        return min(prices, default=None)
