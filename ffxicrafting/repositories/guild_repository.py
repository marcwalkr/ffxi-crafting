from models import GuildVendor, GuildShop


class GuildRepository:
    guild_vendor_cache = {}
    guild_shop_cache = {}

    def __init__(self, db) -> None:
        self.db = db

    def get_guild_vendor(self, guild_id):
        if guild_id in self.guild_vendor_cache:
            return self.guild_vendor_cache[guild_id]
        else:
            guild_tuple = self.db.get_guild_vendor(guild_id)
            if guild_tuple:
                self.guild_vendor_cache[guild_id] = GuildVendor(*guild_tuple)
                return self.guild_vendor_cache[guild_id]
            return None

    def get_guild_shops(self, item_id):
        if item_id in self.guild_shop_cache:
            return self.guild_shop_cache[item_id]
        else:
            guild_shop_tuples = self.db.get_guild_shops(item_id)
            if guild_shop_tuples:
                self.guild_shop_cache[item_id] = [GuildShop(*g) for g in guild_shop_tuples]
                return self.guild_shop_cache[item_id]

            self.guild_shop_cache[item_id] = []
            return []
