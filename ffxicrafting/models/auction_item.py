class AuctionItem:
    """
    Represents an item in the game's auction house.

    This class corresponds to a database table that stores auction-related information
    for items. It includes data about pricing, sales frequency, and listing type.
    """

    def __init__(self, item_id: int, avg_price: float, num_sales: int, sell_frequency: float, is_stack: bool,
                 new_data: bool) -> None:
        """
        Initialize an AuctionItem instance.

        Args:
            item_id (int): The ID of the item being sold.
            average_price (float): The average price of the item in the auction house.
            num_sales (int): The number of sales of this item in the last 15 days.
            sell_frequency (float): The average number of sales per day, based on num_sales.
            is_stack (bool): True if this listing is for a stack of items, False for single items.
            new_data (bool): Flag indicating if new auction data is available in the sales_history table.
        """
        self.item_id: int = item_id
        self.average_price: float = avg_price
        self.num_sales: int = num_sales
        self.sell_frequency: float = sell_frequency
        self.is_stack: bool = is_stack
        self.new_data: bool = new_data
