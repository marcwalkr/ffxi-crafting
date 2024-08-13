from database import Database
from models import ItemModel


class ItemRepository:
    """
    Repository class for handling item-related data operations.

    This class provides methods to interact with the database for retrieving
    item information.
    """

    _cache: list[ItemModel] = []

    def __init__(self, db: Database) -> None:
        """
        Initialize an ItemRepository instance.
        All items are loaded into the cache on initialization.

        Args:
            db (Database): The database connection object used for querying item data.
        """
        self._db: Database = db
        if not ItemRepository._cache:
            self._load_items()

    def _load_items(self) -> None:
        """
        Load all items into the cache.
        """
        all_recipe_item_ids = self._db.get_all_recipe_item_ids()
        item_tuples = self._db.get_items(all_recipe_item_ids)
        item_models = [ItemModel(*tuple) for tuple in item_tuples]
        ItemRepository._cache = item_models

    def get_all_items(self) -> list[ItemModel]:
        """
        Retrieve all ItemModel objects from the cache.

        Returns:
            list[ItemModel]: A list of ItemModel objects corresponding to the requested item IDs.
        """
        return self._cache

    def delete_cache(self) -> None:
        """
        Delete the cache.
        """
        self._cache = []
