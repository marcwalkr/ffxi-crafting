from functools import lru_cache
from database.database import Database
from models.guild_shop import GuildShop


class GuildController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    @lru_cache(maxsize=None)
    def get_guild_shops(cls, item_id):
        guild_shop_tuples = cls.db.get_guild_shops(item_id)
        return [GuildShop(*g) for g in guild_shop_tuples]
