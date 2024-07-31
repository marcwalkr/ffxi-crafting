from models import GuildVendor, GuildShop
from functools import lru_cache


class GuildRepository:
    def __init__(self, db) -> None:
        self.db = db

    @lru_cache(maxsize=None)
    def get_guild_vendor(self, guild_id):
        guild_tuple = self.db.get_guild_vendor(guild_id)
        if guild_tuple:
            return GuildVendor(*guild_tuple)
        else:
            return None

    @lru_cache(maxsize=None)
    def get_guild_shops(self, item_id):
        guild_shop_tuples = self.db.get_guild_shops(item_id)
        if guild_shop_tuples:
            return [GuildShop(*g) for g in guild_shop_tuples]
        else:
            return []
