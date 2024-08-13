from database import Database
from models import GuildVendor, GuildShop


class GuildRepository:
    """
    Repository class for handling guild-related data operations.

    This class provides methods to interact with the database for retrieving
    guild vendor and guild shop data.
    """

    _guild_vendor_cache: dict[int, GuildVendor] = {}
    _guild_shop_cache: dict[int, list[GuildShop]] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize a GuildRepository instance.
        All guild vendor and guild shop data are loaded into the cache on initialization.

        Args:
            db (Database): The database connection object used for querying guild data.
        """
        self._db: Database = db
        if not GuildRepository._guild_vendor_cache:
            self._load_guild_vendors()
        if not GuildRepository._guild_shop_cache:
            self._load_guild_shops()

    def _load_guild_vendors(self) -> None:
        """
        Load all guild vendor data into the cache.
        """
        guild_vendor_tuples = self._db.get_all_guild_vendors()
        guild_vendors = [GuildVendor(*tuple) for tuple in guild_vendor_tuples]
        GuildRepository._guild_vendor_cache.update({g.guild_id: g for g in guild_vendors})

    def _load_guild_shops(self) -> None:
        """
        Load all guild shop data into the cache.
        """
        guild_shop_tuples = self._db.get_all_guild_shops()
        guild_shops = [GuildShop(*tuple) for tuple in guild_shop_tuples]

        # Group guild shops by item_id
        grouped_guild_shops = {}
        for shop in guild_shops:
            if shop.item_id not in grouped_guild_shops:
                grouped_guild_shops[shop.item_id] = []
            grouped_guild_shops[shop.item_id].append(shop)

        GuildRepository._guild_shop_cache = grouped_guild_shops

    def get_guild_vendor(self, guild_id: int) -> GuildVendor | None:
        """
        Retrieve guild vendor information for a given guild ID from the cache.

        Args:
            guild_id (int): The ID of the guild to retrieve vendor information for.

        Returns:
            GuildVendor | None: A GuildVendor object for the given guild ID,
                                or None if no vendor information is found.
        """
        if guild_id in self._guild_vendor_cache:
            return self._guild_vendor_cache[guild_id]
        else:
            return None

    def get_guild_shops(self, item_id: int) -> list[GuildShop]:
        """
        Retrieve guild shop information for a given item ID from the cache.

        Args:
            item_id (int): The ID of the item to retrieve guild shop information for.

        Returns:
            list[GuildShop]: A list of GuildShop objects for the given item ID.
                             Returns an empty list if no guild shops are found.
        """
        if item_id in self._guild_shop_cache:
            return self._guild_shop_cache[item_id]
        else:
            return []
