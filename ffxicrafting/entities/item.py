from models.item_model import ItemModel
from controllers.vendor_controller import VendorController
from controllers.guild_controller import GuildController
from controllers.auction_controller import AuctionController
from config.settings_manager import SettingsManager


class Item(ItemModel):
    def __init__(self, item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell) -> None:
        super().__init__(item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell)
        self.id = item_id
        self.single_price = None
        self.stack_price = None
        self.single_sell_freq = None
        self.stack_sell_freq = None
        self.min_vendor_price = None

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Item):
            return self.item_id == __value.item_id
        return False

    def __hash__(self) -> int:
        return hash(self.item_id)

    def set_auction_data(self):
        auction_data = self.get_auction_data()
        self.single_price, self.stack_price, self.single_sell_freq, self.stack_sell_freq = auction_data

    def set_vendor_data(self):
        self.min_vendor_price = self.get_vendor_data()

    def get_auction_data(self):
        def get_price(is_stack):
            auction_item = AuctionController.get_auction_item(self.item_id, is_stack)
            if auction_item is None or auction_item.avg_price <= 0:
                return None, None
            return auction_item.avg_price, auction_item.sell_freq

        single_price, single_sell_freq = get_price(False)
        stack_price, stack_sell_freq = get_price(True) if self.stack_size > 1 else (None, None)

        return single_price, stack_price, single_sell_freq, stack_sell_freq

    def get_vendor_data(self):
        vendor_items = VendorController.get_vendor_items(self.item_id)
        regional_vendors = VendorController.get_regional_vendors()
        enabled_regional_merchants = SettingsManager.get_enabled_regional_merchants()

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
