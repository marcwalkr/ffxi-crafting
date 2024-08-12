import threading
from controllers import AuctionController, VendorController, GuildController
from database import Database
from entities import Item
from repositories import ItemRepository


class ItemController:
    """
    Controller class for managing item-related operations.

    This class handles operations related to items, including fetching item data
    and updating item information from various sources such as auctions, vendors,
    and guilds.
    """

    _cache = {}
    _cache_lock = threading.Lock()

    def __init__(self, db: Database) -> None:
        """
        Initializes repositories for items, recipes, vendors, and guilds,
        as well as the auction controller.

        Args:
            db (Database): The database connection object.
        """
        self._item_repository: ItemRepository = ItemRepository(db)
        self._auction_controller: AuctionController = AuctionController(db)
        self._vendor_controller: VendorController = VendorController(db)
        self._guild_controller: GuildController = GuildController(db)

    def get_recipe_items(self, item_ids: list[int]) -> list[Item]:
        """
        Fetches item data from the database, converts it to an Item entity, and caches it for future use.

        Args:
            item_ids (list[int]): List of item IDs for the recipe's ingredients and results.

        Returns:
            list[Item]: A list of Item objects.
        """
        item_models = self._item_repository.get_items(item_ids)

        items = []
        with self._cache_lock:
            for item_model in item_models:
                if item_model.item_id in self._cache:
                    items.append(self._cache[item_model.item_id])
                else:
                    item = Item(item_model.item_id, item_model.name, item_model.sort_name, item_model.stack_size)
                    self._cache[item_model.item_id] = item
                    items.append(item)

        return items

    def update_auction_data(self, item_id: int) -> None:
        """
        Fetches the latest auction data for the item and updates the
        corresponding Item entity with this information.

        Args:
            item_id (int): The ID of the item to update auction data for.

        Raises:
            ValueError: If the item is not found in the cache.
        """
        item = self._cache.get(item_id)
        if item:
            if item.min_single_price is None:
                single_auction_data = self._auction_controller.get_auction_data(item_id, is_stack=False)
                if single_auction_data:
                    item.average_single_price = single_auction_data.average_price
                    item.min_single_price = single_auction_data.min_price
                    item.max_single_price = single_auction_data.max_price
                    item.single_sell_frequency = single_auction_data.sell_frequency
            if item.min_stack_price is None:
                stack_auction_data = self._auction_controller.get_auction_data(item_id, is_stack=True)
                if stack_auction_data:
                    item.average_stack_price = stack_auction_data.average_price
                    item.min_stack_price = stack_auction_data.min_price
                    item.max_stack_price = stack_auction_data.max_price
                    item.stack_sell_frequency = stack_auction_data.sell_frequency
        else:
            raise ValueError(f"Item with id {item_id} not found in cache.")

    def update_vendor_cost(self, item_id: int) -> None:
        """
        Fetches the min vendor cost for the item and updates the
        corresponding Item entity with this information.

        Args:
            item_id (int): The ID of the item to update vendor cost for.

        Raises:
            ValueError: If the item is not found in the cache.
        """
        item = self._cache.get(item_id)
        if item:
            item.min_vendor_cost = self._vendor_controller.get_min_cost(item_id)
        else:
            raise ValueError(f"Item with id {item_id} not found.")

    def update_guild_cost(self, item_id: int) -> None:
        """
        Fetches the min guild cost for the item and updates the
        corresponding Item entity with this information.

        Args:
            item_id (int): The ID of the item to update guild costs for.

        Raises:
            ValueError: If the item is not found in the cache.
        """
        item = self._cache.get(item_id)
        if item:
            item.min_guild_cost = self._guild_controller.get_min_cost(item_id)
        else:
            raise ValueError(f"Item with id {item_id} not found.")
