from functools import lru_cache
from database import Database
from models import Guild, GuildShop


class GuildController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    @lru_cache(maxsize=None)
    def get_guild(cls, guild_id):
        guild_tuple = cls.db.get_guild(guild_id)
        if guild_tuple:
            return Guild(*guild_tuple)
        return None

    @classmethod
    @lru_cache(maxsize=None)
    def get_guild_shops(cls, item_id):
        guild_shop_tuples = cls.db.get_guild_shops(item_id)
        return [GuildShop(*g) for g in guild_shop_tuples]
