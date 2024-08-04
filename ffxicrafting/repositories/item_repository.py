from database import Database
from models import ItemModel


class ItemRepository:
    """
    Repository class for handling item-related data operations.

    This class provides methods to interact with the database for retrieving
    item information. It implements caching to improve performance for
    frequently accessed items.
    """

    _cache: dict[int, ItemModel] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize an ItemRepository instance.

        Args:
            db (Database): The database connection object used for querying item data.
        """
        self._db: Database = db

    def get_items(self, item_ids: list[int]) -> list[ItemModel]:
        """
        Retrieve item information for a list of item IDs.

        This method first checks the cache for each requested item. For items not found
        in the cache, it queries the database and caches the results for future use.

        Args:
            item_ids (list[int]): A list of item IDs to retrieve information for.

        Returns:
            list[ItemModel]: A list of ItemModel objects corresponding to the requested item IDs.
                             The list may be smaller than the input list if some items are not found.
        """
        # Get cached items and identify missing items
        cached_items = [self._cache[id] for id in item_ids if id in self._cache]
        missing_item_ids = [id for id in item_ids if id not in self._cache]

        # Fetch missing items from the database
        if missing_item_ids:
            item_tuples = self._db.get_items(missing_item_ids)
            new_items = [ItemModel(*tuple) for tuple in item_tuples]

            # Update cache with new items
            self._cache.update({item.item_id: item for item in new_items})

            return cached_items + new_items

        return cached_items
