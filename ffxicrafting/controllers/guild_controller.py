from database import Database
from models.guild_shop import GuildShop
from models.guild import Guild


class GuildController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_guild_shops(cls, item_id):
        guild_shop_tuples = cls.db.get_guild_shops(item_id)

        guild_shops = []
        for guild_shop_tuple in guild_shop_tuples:
            guild_shop = GuildShop(*guild_shop_tuple)
            guild_shops.append(guild_shop)

        return guild_shops

    @classmethod
    def get_guild(cls, guild_id):
        guild_tuple = cls.db.get_guild(guild_id)

        if guild_tuple is not None:
            return Guild(*guild_tuple)
        else:
            return None
