from database import Database
from repositories import AuctionRepository
from models import AuctionItem, SalesHistory
from entities import AuctionData


class AuctionController:
    """
    Controller class for managing auction-related operations.

    This class serves as an intermediary between the application logic and the
    AuctionRepository, handling operations related to auction items and sales history.
    """

    def __init__(self, db: Database) -> None:
        """
        Initialize the AuctionController.

        Args:
            db: The database connection object.
        """
        self._auction_repository: AuctionRepository = AuctionRepository(db)

    def get_auction_data(self, item_id: int, is_stack: bool) -> AuctionData:
        """
        Fetches the auction data for a given item, specifying if the item is a stack or not.

        Args:
            item_id (int): The ID of the item to retrieve auction data for.
            is_stack (bool): Whether the item is a stack or not.

        Returns:
            AuctionData: The auction data for the given item ID and single/stack category.
        """
        auction_item = self._get_auction_item_with_updates(item_id, is_stack)
        if auction_item:
            sales_history = self._auction_repository.get_latest_sales_history(item_id, is_stack)
            auction_data = AuctionData(auction_item.item_id, auction_item.average_price, auction_item.num_sales,
                                       auction_item.sell_frequency, auction_item.is_stack, auction_item.new_data,
                                       sales_history=sales_history)
            return auction_data
        else:
            return None

    def _get_auction_item_with_updates(self, item_id: int, is_stack: bool) -> AuctionItem:
        """
        Fetches auction items, checks for new data, and updates the items
        with the latest sales history information.

        Args:
            item_id (int): The ID of the item to retrieve auction data for.
            is_stack (bool): Whether the item is a stack or not.
        Returns:
            AuctionItem: The updated AuctionItem object.
        """
        auction_item = self._auction_repository.get_auction_item(item_id, is_stack)
        if auction_item and auction_item.new_data:
            new_sales_history = self._auction_repository.get_latest_sales_history(item_id, is_stack)
            updated_item = self._process_new_data(auction_item, new_sales_history)
            self._auction_repository.update_auction_item(updated_item)
            return updated_item
        else:
            return auction_item

    def _process_new_data(self, item: AuctionItem, new_sales_history: list[SalesHistory]) -> AuctionItem:
        """
        Calculates new average price and sell frequency based on the
        provided sales history data. If no new sales history is provided,
        the item is returned unchanged.

        Args:
            item (AuctionItem): The auction item to update.
            new_sales_history (list[SalesHistory]): List of new sales history entries.

        Returns:
            AuctionItem: The updated AuctionItem with new average price and sell frequency.
        """
        if not new_sales_history:
            return item
        prices = [sale.price for sale in new_sales_history]
        avg_price = sum(prices) / len(prices)
        item.average_price = avg_price
        item.sell_frequency = item.num_sales / 15
        return item
