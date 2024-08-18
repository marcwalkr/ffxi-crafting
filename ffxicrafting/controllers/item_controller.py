from controllers import AuctionController, VendorController, GuildController
from database import Database
from entities import Item
from repositories import ItemRepository


class ItemController:
    """
    Controller class for managing item-related operations.

    This class handles creating, storing, and retrieving Item objects.
    """

    _cache = {}

    def __init__(self, db: Database) -> None:
        """
        Initializes repository for item data and controllers for auction, vendor, and guild data.
        All Item objects are created and cached on initialization.

        Args:
            db (Database): The database connection object.
        """
        self._item_repository: ItemRepository = ItemRepository(db)
        self._auction_controller: AuctionController = AuctionController(db)
        self._vendor_controller: VendorController = VendorController(db)
        self._guild_controller: GuildController = GuildController(db)

        if not ItemController._cache:
            self._create_item_objects()

    def _create_item_objects(self) -> None:
        """
        Create item objects from the item repository and cache them.
        """
        item_models = self._item_repository.get_all_items()
        for item_model in item_models:
            single_auction_data = self._auction_controller.get_auction_data(item_model.item_id, is_stack=False)
            stack_auction_data = self._auction_controller.get_auction_data(item_model.item_id, is_stack=True)

            min_vendor_cost = self._vendor_controller.get_min_cost(item_model.item_id)
            min_guild_cost = self._guild_controller.get_min_cost(item_model.item_id)

            item = Item(item_model.item_id, item_model.name, item_model.sort_name, item_model.stack_size,
                        single_auction_data, stack_auction_data, min_vendor_cost, min_guild_cost)
            ItemController._cache[item_model.item_id] = item

        self._item_repository.delete_cache()

    def get_recipe_items(self, item_ids: list[int]) -> list[Item]:
        """
        Fetches Item objects with the given item IDs from the cache.

        Args:
            item_ids (list[int]): List of item IDs for the recipe's ingredients and results.

        Returns:
            list[Item]: A list of Item objects.
        """
        return [self._cache[item_id] for item_id in item_ids]
