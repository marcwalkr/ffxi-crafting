from threading import Lock
from models import AuctionItem, SalesHistory
from database import Database


class AuctionRepository:
    """
    Repository class for handling auction-related data operations.

    This class provides methods to interact with the database for retrieving
    and updating auction items and sales history data. It implements caching
    to improve performance for frequently accessed auction items.
    """

    _auction_item_cache: dict[tuple[int, bool], AuctionItem] = {}
    _sales_history_cache: dict[tuple[int, bool], list[SalesHistory]] = {}
    _cache_lock: Lock = Lock()

    def __init__(self, db: Database) -> None:
        """
        Initialize an AuctionRepository instance.

        Args:
            db (Database): The database connection object used for querying auction data.
        """
        self._db: Database = db

    def get_auction_item(self, item_id: int, is_stack: bool) -> AuctionItem | None:
        """
        Retrieve auction items for a given item ID.

        This method first checks the cache for the requested item. If not found,
        it queries the database and caches the result for future use.

        Args:
            item_id (int): The ID of the item to retrieve auction data for.
            is_stack (bool): Indicates whether to retrieve data for stacks (True) or singles (False).
        Returns:
            AuctionItem | None: An AuctionItem object for the given item ID.
            Returns None if no auction item was found.
        """
        cache_key = (item_id, is_stack)
        if cache_key in self._auction_item_cache:
            return self._auction_item_cache[cache_key]
        else:
            auction_item_tuple = self._db.get_auction_item(item_id, is_stack)
            if auction_item_tuple is not None:
                auction_item = AuctionItem(*auction_item_tuple)
                self._auction_item_cache[cache_key] = auction_item
                return auction_item
            else:
                self._auction_item_cache[cache_key] = None
                return None

    def update_auction_item(self, new_item: AuctionItem) -> None:
        """
        Update an auction item in the database and cache.

        This method updates the auction item data in the database and invalidates
        the cache with the item id.

        Args:
            new_item (AuctionItem): The AuctionItem object with updated information.
        """
        self._db.update_auction_item(new_item.item_id, new_item.avg_price, new_item.sell_freq, new_item.is_stack)
        self._invalidate_cache(new_item.item_id)

    def get_latest_sales_history(self, item_id: int, is_stack: bool) -> list[SalesHistory]:
        """
        Retrieve the latest sales history for a given item.

        This method first checks the cache for the requested item. If not found,
        it queries the database and caches the result for future use.

        Args:
            item_id (int): The ID of the item to retrieve sales history for.
            is_stack (bool): Whether to retrieve history for stacks or single items.

        Returns:
            list[SalesHistory]: A list of SalesHistory objects representing the latest sales.
                                Returns an empty list if no sales history is found.
        """
        cache_key = (item_id, is_stack)
        if cache_key in self._sales_history_cache:
            return self._sales_history_cache[cache_key]
        else:
            sales_history_tuples = self._db.get_latest_sales_history(item_id, is_stack)
            if sales_history_tuples:
                sales_history_list = [SalesHistory(*sales_history_tuple)
                                      for sales_history_tuple in sales_history_tuples]
                self._sales_history_cache[cache_key] = sales_history_list
                return sales_history_list
            else:
                self._sales_history_cache[cache_key] = []
                return []

    def _invalidate_cache(self, item_id: int) -> None:
        """
        Invalidate the cache for a given item ID.
        """
        with self._cache_lock:
            self._auction_item_cache.pop(item_id, None)
