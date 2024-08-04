class SalesHistory:
    """
    Represents a single sale transaction in the game's auction house.

    This class corresponds to a database table that stores historical sales data
    obtained from parsing the game's website.
    """

    def __init__(self, id: int, item_id: int, sell_date: int, buyer: str, seller: str, price: int, batch_id: int,
                 is_stack: bool) -> None:
        """
        Initialize a SalesHistory instance.

        Args:
            id (int): The unique identifier for this sales record.
            item_id (int): The ID of the item that was sold.
            sell_date (int): The Unix timestamp representing when the sale occurred.
            buyer (str): The character name of the player who bought the item.
            seller (str): The character name of the player who sold the item.
            price (int): The price at which the item was sold.
            batch_id (int): An identifier grouping sales records that were parsed together.
            is_stack (bool): True if this sale was for a stack of items, False for a single item.

        The batch_id is used to group sales records that were obtained from the same
        parsing session of the game's website. This helps in identifying and managing
        data that was collected at approximately the same time.
        """
        self.id: int = id
        self.item_id: int = item_id
        self.sell_date: int = sell_date
        self.buyer: str = buyer
        self.seller: str = seller
        self.price: int = price
        self.batch_id: int = batch_id
        self.is_stack: bool = is_stack
