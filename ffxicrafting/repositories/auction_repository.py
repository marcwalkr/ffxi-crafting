from models import AuctionItem, SalesHistory
from database import Database


class AuctionRepository:
    """
    Repository class for handling auction-related data operations.

    This class provides methods to interact with the database for retrieving
    and updating auction items and sales history data. It implements caching
    to improve performance for frequently accessed auction items.
    """

    _cache: dict[int, list[AuctionItem]] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize an AuctionRepository instance.

        Args:
            db (Database): The database connection object used for querying auction data.
        """
        self._db: Database = db

    def get_auction_items(self, item_id: int) -> list[AuctionItem]:
        """
        Retrieve auction items for a given item ID.

        This method first checks the cache for the requested item. If not found,
        it queries the database and caches the result for future use.

        Args:
            item_id (int): The ID of the item to retrieve auction data for.

        Returns:
            list[AuctionItem]: A list of AuctionItem objects for the given item ID.
                               Returns an empty list if no auction items are found.
        """
        if item_id in self._cache:
            return self._cache[item_id]
        else:
            auction_item_tuples = self._db.get_auction_items(item_id)
            if auction_item_tuples is not None:
                auction_items = [AuctionItem(*auction_item_tuple) for auction_item_tuple in auction_item_tuples]
                self._cache[item_id] = auction_items
                return auction_items
            else:
                self._cache[item_id] = []
                return []

    def update_auction_item(self, new_item: AuctionItem) -> None:
        """
        Update an auction item in the database and cache.

        This method updates the auction item data in the database and refreshes
        the cache with the new information.

        Args:
            new_item (AuctionItem): The AuctionItem object with updated information.
        """
        self._db.update_auction_item(new_item.item_id, new_item.avg_price, new_item.sell_freq, new_item.is_stack)
        self._cache[new_item.item_id] = new_item

    def get_latest_sales_history(self, item_id: int, is_stack: bool) -> list[SalesHistory]:
        """
        Retrieve the latest sales history for a given item.

        This method queries the database for the most recent sales history
        entries for the specified item.

        Args:
            item_id (int): The ID of the item to retrieve sales history for.
            is_stack (bool): Whether to retrieve history for stacks or single items.

        Returns:
            list[SalesHistory]: A list of SalesHistory objects representing the latest sales.
                                Returns an empty list if no sales history is found.
        """
        sales_history_tuples = self._db.get_latest_sales_history(item_id, is_stack)
        if sales_history_tuples:
            sales_history_list = [SalesHistory(*sales_history_tuple) for sales_history_tuple in sales_history_tuples]
            return sales_history_list
        else:
            return []
