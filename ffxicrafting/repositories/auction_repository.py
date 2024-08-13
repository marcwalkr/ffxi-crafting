from threading import Lock
from models import AuctionItem, SalesHistory
from database import Database


class AuctionRepository:
    """
    Repository class for handling auction-related data operations.

    This class provides methods to interact with the database for retrieving
    and updating auction items and sales history data.
    """

    _sales_history_cache: dict[tuple[int, bool], list[SalesHistory]] = {}
    _auction_item_cache: dict[tuple[int, bool], AuctionItem] = {}
    _cache_lock: Lock = Lock()

    def __init__(self, db: Database) -> None:
        """
        Initialize an AuctionRepository instance.
        All sales history and auction items are loaded into the cache on initialization.

        Args:
            db (Database): The database connection object used for querying auction data.
        """
        self._db: Database = db
        if not AuctionRepository._sales_history_cache:
            self._load_sales_history()
        if not AuctionRepository._auction_item_cache:
            self._load_auction_items()

    def _load_sales_history(self) -> None:
        """
        Load all sales history into the cache, keeping only the latest batch for each item.
        """
        sales_history_tuples = self._db.get_all_sales_history()
        sales_history = [SalesHistory(*tuple) for tuple in sales_history_tuples]

        # Group sales history by (item_id, is_stack) and keep only the latest batch
        grouped_history = {}
        for item in sales_history:
            key = (item.item_id, item.is_stack)
            if key not in grouped_history or item.batch_id > grouped_history[key][0].batch_id:
                grouped_history[key] = [item]
            elif item.batch_id == grouped_history[key][0].batch_id:
                grouped_history[key].append(item)

        # Update the cache with grouped history
        AuctionRepository._sales_history_cache = grouped_history

    def _load_auction_items(self) -> None:
        """
        Load all auction items into the cache.
        """
        auction_item_tuples = self._db.get_all_auction_items()
        auction_items = [AuctionItem(*tuple) for tuple in auction_item_tuples]
        AuctionRepository._auction_item_cache.update({(item.item_id, item.is_stack): item for item in auction_items})

    def get_latest_sales_history(self, item_id: int, is_stack: bool) -> list[SalesHistory]:
        """
        Retrieve the latest sales history for a given item from the cache.

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
            return []

    def get_auction_item(self, item_id: int, is_stack: bool) -> AuctionItem | None:
        """
        Retrieve an AuctionItem object from the cache.

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
            return None

    def update_auction_item(self, new_item: AuctionItem) -> None:
        """
        Update an auction item in the cache.

        Args:
            new_item (AuctionItem): The AuctionItem object with updated information.
        """
        with self._cache_lock:
            cache_key = (new_item.item_id, new_item.is_stack)
            self._auction_item_cache[cache_key] = new_item
