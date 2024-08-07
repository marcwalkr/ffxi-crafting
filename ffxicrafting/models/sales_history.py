class SalesHistory:
    """
    Represents a single sale transaction in the game's auction house.

    This class corresponds to a database table that stores historical sales data
    obtained from parsing the game's website.
    """

    def __init__(self, item_id: int, price: int, is_stack: bool) -> None:
        """
        Initialize a SalesHistory instance.

        Args:
            item_id (int): The ID of the item that was sold.
            price (int): The price at which the item was sold.
            is_stack (bool): True if this sale was for a stack of items, False for a single item.
        """
        self.item_id: int = item_id
        self.price: int = price
        self.is_stack: bool = is_stack
