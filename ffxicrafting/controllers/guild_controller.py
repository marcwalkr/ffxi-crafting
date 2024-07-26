from models import GuildVendor, GuildShop


class GuildController:
    cache = {
        "get_guild_vendor": {},
        "get_guild_shops": {}
    }

    def __init__(self, db) -> None:
        self.db = db

    def get_guild_vendor(self, guild_id):
        if guild_id in self.cache["get_guild_vendor"]:
            return self.cache["get_guild_vendor"][guild_id]
        else:
            guild_tuple = self.db.get_guild_vendor(guild_id)
            if guild_tuple:
                self.cache["get_guild_vendor"][guild_id] = GuildVendor(*guild_tuple)
                return self.cache["get_guild_vendor"][guild_id]
            return None

    def get_guild_shops(self, item_id):
        if item_id in self.cache["get_guild_shops"]:
            return self.cache["get_guild_shops"][item_id]
        else:
            guild_shop_tuples = self.db.get_guild_shops(item_id)
            if guild_shop_tuples:
                self.cache["get_guild_shops"][item_id] = [GuildShop(*g) for g in guild_shop_tuples]
                return self.cache["get_guild_shops"][item_id]

            self.cache["get_guild_shops"][item_id] = []
            return []
