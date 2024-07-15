from functools import lru_cache
from models.item_model import ItemModel
from controllers.vendor_controller import VendorController
from controllers.guild_controller import GuildController
from controllers.auction_controller import AuctionController
from config.settings_manager import SettingsManager


class Item(ItemModel):
    def __init__(self, item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell) -> None:
        super().__init__(item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell)
        self.id = item_id
        self.min_price = self.get_min_price()
        self.min_vendor_price = self.get_min_vendor_price()
        self.single_price, self.stack_price = self.get_auction_prices()

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Item):
            return self.item_id == __value.item_id
        return False

    def __hash__(self) -> int:
        return hash(self.item_id)

    @lru_cache(maxsize=None)
    def get_min_price(self):
        prices = [
            self.get_min_auction_price(),
            self.get_min_vendor_price(),
            self.get_guild_price()
        ]
        prices = [price for price in prices if price is not None]
        return min(prices, default=None)

    @lru_cache(maxsize=None)
    def get_auction_prices(self):
        auction_item = AuctionController.get_auction_item(self.item_id)
        if not auction_item:
            return None, None

        single_price = auction_item.single_price if auction_item.single_price > 0 else None
        stack_price = auction_item.stack_price if auction_item.stack_price > 0 else None

        return single_price, stack_price

    def get_min_auction_price(self):
        single_price, stack_price = self.get_auction_prices()

        # Calculate stack price per item if stack price is available
        stack_price_per_item = (stack_price / self.stack_size) if stack_price is not None else None

        # Filter out None values and find the minimum price
        prices = [price for price in [single_price, stack_price_per_item] if price is not None]

        return min(prices, default=None)

    @lru_cache(maxsize=None)
    def get_min_vendor_price(self):
        vendor_items = VendorController.get_vendor_items(self.item_id)
        regional_vendors = VendorController.get_regional_vendors()
        enabled_regional_merchants = SettingsManager.get_enabled_regional_merchants()

        # Create a list of vendor items including items from non-regional vendors
        # and items from regional vendors if the vendor is included in enabled regional merchants
        filtered_vendor_items = []
        regional_vendor_ids = {vendor.npc_id: vendor.region for vendor in regional_vendors}

        for vendor_item in vendor_items:
            vendor_region = regional_vendor_ids.get(vendor_item.npc_id)
            if vendor_region is None or vendor_region in enabled_regional_merchants:
                filtered_vendor_items.append(vendor_item)

        prices = [vendor_item.price for vendor_item in filtered_vendor_items]

        guild_price = self.get_guild_price()
        if guild_price is not None:
            prices.append(guild_price)

        return min(prices, default=None)

    def get_guild_price(self):
        enabled_guilds = SettingsManager.get_enabled_guilds()
        guild_shops = GuildController.get_guild_shops(self.item_id)
        prices = []

        for shop in guild_shops:
            if shop.initial_quantity > 0:
                guild = GuildController.get_guild(shop.guild_id)
                if guild and guild.category in enabled_guilds:
                    prices.append(shop.min_price)

        return min(prices, default=None)

    def get_formatted_name(self):
        return self.sort_name.replace("_", " ").title()
