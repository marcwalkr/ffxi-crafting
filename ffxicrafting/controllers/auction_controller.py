from database import Database
from repositories import AuctionRepository
from models import AuctionItem, SalesHistory


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

    def get_auction_items_with_updates(self, item_id: int) -> list[AuctionItem]:
        """
        Fetches auction items, checks for new data, and updates the items
        with the latest sales history information.

        Args:
            item_id (int): The ID of the item to retrieve auction data for.

        Returns:
            list[AuctionItem]: A list of updated AuctionItem objects.
        """
        updated_auction_items = []
        auction_items = self._auction_repository.get_auction_items(item_id)
        for item in auction_items:
            if item.new_data:
                new_sales_history = self._auction_repository.get_latest_sales_history(item.item_id, item.is_stack)
                updated_item = self._process_new_data(item, new_sales_history)
                self._auction_repository.update_auction_item(updated_item)
                updated_auction_items.append(updated_item)
            else:
                updated_auction_items.append(item)
        return updated_auction_items

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
        item.avg_price = avg_price
        item.sell_frequency = item.num_sales / 15
        return item
