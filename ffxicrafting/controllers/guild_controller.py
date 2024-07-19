from models import Guild, GuildShop


class GuildController:
    _cache = {
        "get_guild": {},
        "get_guild_shops": {}
    }

    def __init__(self, db) -> None:
        self.db = db

    def get_guild(self, guild_id):
        if guild_id in self._cache["get_guild"]:
            return self._cache["get_guild"][guild_id]
        else:
            guild_tuple = self.db.get_guild(guild_id)
            if guild_tuple:
                self._cache["get_guild"][guild_id] = Guild(*guild_tuple)
                return self._cache["get_guild"][guild_id]
            return None

    def get_guild_shops(self, item_id):
        if item_id in self._cache["get_guild_shops"]:
            return self._cache["get_guild_shops"][item_id]
        else:
            guild_shop_tuples = self.db.get_guild_shops(item_id)
            if guild_shop_tuples:
                self._cache["get_guild_shops"][item_id] = [GuildShop(*g) for g in guild_shop_tuples]
                return self._cache["get_guild_shops"][item_id]

            self._cache["get_guild_shops"][item_id] = []
            return []
