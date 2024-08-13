class SalesHistory:
    """
    Represents a single sale transaction in the game's auction house.

    This class corresponds to a database table that stores historical sales data
    obtained from parsing the game's website.
    """

    def __init__(self, item_id: int, is_stack: bool, price: int, batch_id: int) -> None:
        """
        Initialize a SalesHistory instance.

        Args:
            item_id (int): The ID of the item that was sold.
            is_stack (bool): True if this sale was for a stack of items, False for a single item.
            price (int): The price at which the item was sold.
            batch_id (int): The ID of the batch which groups sales history based on when they were parsed.
        """
        self.item_id: int = item_id
        self.is_stack: bool = is_stack
        self.price: int = price
        self.batch_id: int = batch_id
