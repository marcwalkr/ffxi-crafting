import threading
from entities import Item, Result, Ingredient, CraftableIngredient
from config import SettingsManager
from repositories import VendorRepository, GuildRepository
from controllers import AuctionController


class ItemController:
    cache = {}
    cache_lock = threading.Lock()

    def __init__(self, db) -> None:
        self.db = db
        self.vendor_repository = VendorRepository(db)
        self.guild_repository = GuildRepository(db)
        self.auction_controller = AuctionController(db)

    def get_items(self, item_ids):
        items = []
        missing_item_ids = []

        # Read from cache and identify missing items
        with self.cache_lock:
            for item_id in item_ids:
                if item_id in self.cache:
                    items.append(self.cache[item_id])
                else:
                    missing_item_ids.append(item_id)

        # If there are missing items, fetch them from the database
        if missing_item_ids:
            item_tuples = self.db.get_items(missing_item_ids)
            if item_tuples:
                with self.cache_lock:
                    for item_tuple in item_tuples:
                        item = Item(*item_tuple)
                        if item.item_id not in self.cache:  # Double-check before adding
                            self.cache[item.item_id] = item
                        items.append(self.cache[item.item_id])

        return items

    def get_item(self, item_id):
        if item_id in self.cache:
            return self.cache[item_id]
        else:
            raise ValueError(f"Item with id {item_id} not found in cache.")

    def convert_to_ingredient(self, item, craftable):
        # Convert the Item object to CraftableIngredient if it's craftable, otherwise convert to Ingredient
        with self.cache_lock:
            if isinstance(self.cache[item.item_id], Ingredient):
                return self.cache[item.item_id]

            if craftable:
                ingredient = CraftableIngredient(item.item_id, item.sub_id, item.name, item.sort_name, item.stack_size, item.flags, item.ah,
                                                 item.no_sale, item.base_sell)
            else:
                ingredient = Ingredient(item.item_id, item.sub_id, item.name, item.sort_name, item.stack_size, item.flags, item.ah,
                                        item.no_sale, item.base_sell)
            # Replace the existing Item object in the cache with the new Ingredient object
            self.cache[item.item_id] = ingredient
        return ingredient

    def convert_to_result(self, item):
        result = Result(item.item_id, item.sub_id, item.name, item.sort_name, item.stack_size, item.flags, item.ah,
                        item.no_sale, item.base_sell)
        return result

    def update_auction_data(self, item_id):
        item = self.get_item(item_id)
        if item.single_price is None or item.stack_price is None or item.single_sell_freq is None or item.stack_sell_freq is None:
            auction_data = self.get_auction_data(item_id)
            single_price, stack_price, single_sell_freq, stack_sell_freq = auction_data

            item.single_price = single_price if single_price is not None else None
            item.stack_price = stack_price if stack_price is not None else None
            item.single_sell_freq = single_sell_freq if single_sell_freq is not None else None
            item.stack_sell_freq = stack_sell_freq if stack_sell_freq is not None else None

        self.sync_results(item)

    def update_vendor_cost(self, item_id):
        ingredient = self.get_item(item_id)
        if ingredient:
            ingredient.vendor_cost = self.get_vendor_cost(item_id)
        else:
            raise ValueError(f"Ingredient with id {item_id} not found.")

    def update_guild_cost(self, item_id):
        ingredient = self.get_item(item_id)
        if ingredient:
            ingredient.guild_cost = self.get_guild_cost(item_id)
        else:
            raise ValueError(f"Ingredient with id {item_id} not found.")

    def get_auction_data(self, item_id):
        auction_items = self.auction_controller.get_auction_items_with_updates(item_id)
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

    def get_vendor_cost(self, item_id):
        vendor_items = self.vendor_repository.get_vendor_items(item_id)
        beastmen_regions = SettingsManager.get_beastmen_regions()

        # Filter out regional vendors that are controlled by Beastmen
        filtered_vendor_items = []
        for vendor_item in vendor_items:
            regional_vendor = self.vendor_repository.get_regional_vendor(vendor_item.npc_id)
            if not regional_vendor:
                # Standard vendor
                filtered_vendor_items.append(vendor_item)
            else:
                vendor_region = regional_vendor.region.lower()
                if vendor_region not in beastmen_regions:
                    filtered_vendor_items.append(vendor_item)

        prices = [vendor_item.price for vendor_item in filtered_vendor_items]

        return min(prices, default=None)

    def get_guild_cost(self, item_id):
        enabled_guilds = SettingsManager.get_enabled_guilds()
        guild_shops = self.guild_repository.get_guild_shops(item_id)
        prices = []

        for shop in guild_shops:
            if shop.initial_quantity > 0:
                guild_vendor = self.guild_repository.get_guild_vendor(shop.guild_id)
                if guild_vendor and guild_vendor.category in enabled_guilds:
                    prices.append(shop.min_price)

        return min(prices, default=None)

    def sync_results(self, item):
        # Sync the changes to any Result object created from this Item
        for result in Result.instances:
            if result.item_id == item.item_id:
                result.update_from_item(item)
