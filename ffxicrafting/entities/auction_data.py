from models import AuctionItem, SalesHistory


class AuctionData(AuctionItem):
    """
    Represents an item in the game's auction house.
    Inherits all attributes from AuctionItem and adds min_price and max_price,
    utilizing the sales history for the item.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize an AuctionData instance.

        Args:
            *args: Variable length argument list for AuctionItem attributes.
            **kwargs: Arbitrary keyword arguments for AuctionItem attributes.
                Expects "sales_history" in kwargs.

        Attributes:
            sales_history (list[SalesHistory]): A list of individual sales for the item.
            min_price (float): The minimum price from the sales history.
            max_price (float): The maximum price from the sales history.
        """
        super().__init__(*args)
        self._sales_history: list[SalesHistory] = kwargs.get("sales_history", [])
        self.min_price: float = self.get_min_price()
        self.max_price: float = self.get_max_price()

    def get_min_price(self) -> float:
        """
        Get the minimum price from the sales history.
        """
        return min(self._sales_history, key=lambda x: x.price).price

    def get_max_price(self) -> float:
        """
        Get the maximum price from the sales history.
        """
        return max(self._sales_history, key=lambda x: x.price).price
