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
        self.min_price = None

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Item):
            return self.item_id == __value.item_id
        return False

    def __hash__(self) -> int:
        return hash(self.item_id)

    def set_auction_data(self):
        if self.single_price is None or self.stack_price is None or self.single_sell_freq is None or self.stack_sell_freq is None:
            auction_data = self.get_auction_data()
            single_price, stack_price, single_sell_freq, stack_sell_freq = auction_data

            if self.stack_size > 1 and stack_price is not None:
                single_price_from_stack = int(stack_price / self.stack_size)
            else:
                single_price_from_stack = None

            self.single_price = int(single_price) if single_price is not None else 0
            self.stack_price = int(stack_price) if stack_price is not None else 0
            self.single_sell_freq = float(f"{single_sell_freq:.4f}") if single_sell_freq is not None else 0
            self.stack_sell_freq = float(f"{stack_sell_freq:.4f}") if stack_sell_freq is not None else 0

            # Determine the minimum auction price, ignoring 0 values
            prices_to_check = [self.single_price, single_price_from_stack]
            min_auction_price = min((price for price in prices_to_check if price not in (None, 0)), default=None)

            # Update min_price if the new min_auction_price is lower
            if min_auction_price is not None and (self.min_price is None or min_auction_price < self.min_price):
                self.min_price = min_auction_price

    def set_vendor_data(self):
        self.min_vendor_price = self.get_vendor_data()

        # Update min_price if the min_vendor_price is lower
        if self.min_vendor_price is not None and (self.min_price is None or self.min_vendor_price < self.min_price):
            self.min_price = self.min_vendor_price

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
