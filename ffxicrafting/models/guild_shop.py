class GuildShop:
    """
    Represents a guild shop item in the game.

    This class corresponds to a database table that stores information about items
    sold in guild shops, including their pricing and stock management details.
    """

    def __init__(self, guild_id: int, item_id: int, min_price: int, max_price: int, max_quantity: int,
                 daily_increase: int, initial_quantity: int) -> None:
        """
        Initialize a GuildShop instance.

        Args:
            guild_id (int): The ID of the guild selling this item.
            item_id (int): The ID of the item being sold.
            min_price (int): The minimum price of the item in the guild shop.
            max_price (int): The maximum price of the item in the guild shop.
            max_quantity (int): The maximum stock quantity of the item in the guild shop.
            daily_increase (int): The amount by which the stock increases each day.
            initial_quantity (int): The initial stock quantity when the guild shop is restocked.

        The max_quantity, daily_increase, and initial_quantity are related to the guild's stock management:
        - The stock starts at initial_quantity.
        - It can increase by daily_increase each day, up to max_quantity.
        - The stock can be depleted if players buy all available items.
        """
        self.guild_id: int = guild_id
        self.item_id: int = item_id
        self.min_price: int = min_price
        self.max_price: int = max_price
        self.max_quantity: int = max_quantity
        self.daily_increase: int = daily_increase
        self.initial_quantity: int = initial_quantity
