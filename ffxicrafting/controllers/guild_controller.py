from database import Database
from repositories import GuildRepository


class GuildController:
    """
    Controller for managing guild shop operations.

    This class provides methods to interact with guild shops,
    including retrieving pricing information for items.
    """

    def __init__(self, db: Database) -> None:
        """
        Initialize the GuildController with a database connection.

        Args:
            db (Database): The database instance for accessing guild data.
        """
        self._guild_repository: GuildRepository = GuildRepository(db)

    def get_min_cost(self, item_id: int) -> int | None:
        """
        Retrieve the minimum cost of an item from all guild shops.

        This method considers only shops that regularly restock the item
        (i.e., have both initial quantity and daily increase greater than 0).

        Args:
            item_id (int): The unique identifier of the item.

        Returns:
            int | None: The minimum price of the item across all eligible guild shops.
                        Returns None if no eligible shops are found.
        """
        guild_shops = self._guild_repository.get_guild_shops(item_id)
        prices = []

        for shop in guild_shops:
            # Check if the item is regularly restocked
            if shop.initial_quantity > 0 and shop.daily_increase > 0:
                prices.append(shop.min_price)

        return min(prices, default=None)
