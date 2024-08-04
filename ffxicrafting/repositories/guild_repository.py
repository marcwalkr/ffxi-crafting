from database import Database
from models import GuildVendor, GuildShop


class GuildRepository:
    """
    Repository class for handling guild-related data operations.

    This class provides methods to interact with the database for retrieving
    guild vendor and guild shop data. It implements caching to improve
    performance for frequently accessed guild information.
    """

    _guild_vendor_cache: dict[int, GuildVendor] = {}
    _guild_shop_cache: dict[int, list[GuildShop]] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize a GuildRepository instance.

        Args:
            db (Database): The database connection object used for querying guild data.
        """
        self._db: Database = db

    def get_guild_vendor(self, guild_id: int) -> GuildVendor | None:
        """
        Retrieve guild vendor information for a given guild ID.

        This method first checks the cache for the requested guild vendor. If not found,
        it queries the database and caches the result for future use.

        Args:
            guild_id (int): The ID of the guild to retrieve vendor information for.

        Returns:
            GuildVendor | None: A GuildVendor object for the given guild ID,
                                or None if no vendor information is found.
        """
        if guild_id in self._guild_vendor_cache:
            return self._guild_vendor_cache[guild_id]
        else:
            guild_tuple = self._db.get_guild_vendor(guild_id)
            if guild_tuple:
                self._guild_vendor_cache[guild_id] = GuildVendor(*guild_tuple)
                return self._guild_vendor_cache[guild_id]
            return None

    def get_guild_shops(self, item_id: int) -> list[GuildShop]:
        """
        Retrieve guild shop information for a given item ID.

        This method first checks the cache for the requested guild shops. If not found,
        it queries the database and caches the result for future use.

        Args:
            item_id (int): The ID of the item to retrieve guild shop information for.

        Returns:
            list[GuildShop]: A list of GuildShop objects for the given item ID.
                             Returns an empty list if no guild shops are found.
        """
        if item_id in self._guild_shop_cache:
            return self._guild_shop_cache[item_id]
        else:
            guild_shop_tuples = self._db.get_guild_shops(item_id)
            if guild_shop_tuples:
                self._guild_shop_cache[item_id] = [GuildShop(*g) for g in guild_shop_tuples]
                return self._guild_shop_cache[item_id]

            self._guild_shop_cache[item_id] = []
            return []
