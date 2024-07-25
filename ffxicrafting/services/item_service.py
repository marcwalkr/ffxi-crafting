from entities import Item, Result, Ingredient
from config import SettingsManager
from controllers import AuctionController, VendorController, GuildController


class ItemService:
    item_cache = {}
    ingredient_cache = {}

    def __init__(self, db) -> None:
        self.db = db
        self.auction_controller = AuctionController(db)
        self.vendor_controller = VendorController(db)
        self.guild_controller = GuildController(db)

    def get_items(self, item_ids):
        # Identify the missing item_ids (those not in the cache)
        missing_item_ids = [item_id for item_id in item_ids if item_id not in self.item_cache]

        # Query the database only for the missing items
        if missing_item_ids:
            item_tuples = self.db.get_items(missing_item_ids)
            if item_tuples:
                for item_tuple in item_tuples:
                    item = Item(*item_tuple)
                    self.item_cache[item.item_id] = item

        # Retrieve all items from the cache
        items = [self.item_cache[item_id] for item_id in item_ids if item_id in self.item_cache]
        return items

    def get_item(self, item_id):
        if item_id in self.item_cache:
            return self.item_cache[item_id]
        else:
            raise ValueError(f"Item with id {item_id} not found in cache.")

    def convert_to_result(self, item):
        result = Result(item.item_id, item.sub_id, item.name, item.sort_name, item.stack_size, item.flags, item.ah,
                        item.no_sale, item.base_sell)
        return result

    def convert_to_ingredient(self, item):
        if item.item_id in self.ingredient_cache:
            return self.ingredient_cache[item.item_id]
        else:
            ingredient = Ingredient(item.item_id, item.sub_id, item.name, item.sort_name, item.stack_size, item.flags, item.ah,
                                    item.no_sale, item.base_sell)
            self.ingredient_cache[item.item_id] = ingredient
            return ingredient

    def update_auction_data(self, item_id):
        item = self.get_item(item_id)
        if item.single_price is None or item.stack_price is None or item.single_sell_freq is None or item.stack_sell_freq is None:
            auction_data = self.get_auction_data(item_id)
            single_price, stack_price, single_sell_freq, stack_sell_freq = auction_data

            item.single_price = int(single_price) if single_price is not None else None
            item.stack_price = int(stack_price) if stack_price is not None else None
            item.single_sell_freq = float(f"{single_sell_freq:.4f}") if single_sell_freq is not None else None
            item.stack_sell_freq = float(f"{stack_sell_freq:.4f}") if stack_sell_freq is not None else None

        self.sync_results(item)
        self.sync_ingredients(item)

    def update_vendor_cost(self, item_id):
        ingredient = self.get_ingredient(item_id)
        if ingredient:
            ingredient.vendor_cost = self.get_vendor_cost(item_id)
        else:
            raise ValueError(f"Ingredient with id {item_id} not found.")

    def update_guild_cost(self, item_id):
        ingredient = self.get_ingredient(item_id)
        if ingredient:
            ingredient.guild_cost = self.get_guild_cost(item_id)
        else:
            raise ValueError(f"Ingredient with id {item_id} not found.")

    def get_auction_data(self, item_id):
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

    def get_vendor_cost(self, item_id):
        vendor_items = self.vendor_controller.get_vendor_items(item_id)
        regional_merchants = SettingsManager.get_regional_merchants()

        # Filter out regional vendors that are controlled by Beastmen
        filtered_vendor_items = []
        for vendor_item in vendor_items:
            regional_vendor = self.vendor_controller.get_regional_vendor(vendor_item.npc_id)
            if not regional_vendor:
                # Standard vendor
                filtered_vendor_items.append(vendor_item)
            else:
                # Format region name to match database
                region_name = regional_vendor.region.lower()
                settings_region = region_name.replace(' ', '_')

                if settings_region in regional_merchants and regional_merchants[settings_region] != "Beastmen":
                    filtered_vendor_items.append(vendor_item)

        # Extract prices from filtered vendor items
        prices = [vendor_item.price for vendor_item in filtered_vendor_items]

        return min(prices, default=None)

    def get_guild_cost(self, item_id):
        enabled_guilds = SettingsManager.get_enabled_guilds()
        guild_shops = self.guild_controller.get_guild_shops(item_id)
        prices = []

        for shop in guild_shops:
            if shop.initial_quantity > 0:
                guild_vendor = self.guild_controller.get_guild_vendor(shop.guild_id)
                if guild_vendor and guild_vendor.category in enabled_guilds:
                    prices.append(shop.min_price)

        return min(prices, default=None)

    def get_ingredient(self, item_id):
        for ingredient in Ingredient.instances:
            if ingredient.item_id == item_id:
                return ingredient
        return None

    def sync_results(self, item):
        # Sync the changes to any Result object created from this Item
        for result in Result.instances:
            if result.item_id == item.item_id:
                result.update_from_item(item)

    def sync_ingredients(self, item):
        # Sync the changes to any Ingredient object created from this Item
        for ingredient in Ingredient.instances:
            if ingredient.item_id == item.item_id:
                ingredient.update_from_item(item)
