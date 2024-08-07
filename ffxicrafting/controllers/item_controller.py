import threading
from config import SettingsManager
from controllers import AuctionController
from database import Database
from entities import Result, Ingredient, CraftableIngredient
from models import ItemModel
from repositories import ItemRepository, RecipeRepository, VendorRepository, GuildRepository


class ItemController:
    """
    Controller class for managing item-related operations.

    This class handles operations related to items, including fetching item data,
    converting between different item representations, and updating item information
    from various sources such as auctions, vendors, and guilds.
    """

    _ingredient_cache = {}
    _cache_lock = threading.Lock()

    def __init__(self, db: Database) -> None:
        """
        Initializes repositories for items, recipes, vendors, and guilds,
        as well as the auction controller.

        Args:
            db (Database): The database connection object.
        """
        self._item_repository: ItemRepository = ItemRepository(db)
        self._recipe_repository: RecipeRepository = RecipeRepository(db)
        self._vendor_repository: VendorRepository = VendorRepository(db)
        self._guild_repository: GuildRepository = GuildRepository(db)
        self._auction_controller: AuctionController = AuctionController(db)

    def get_recipe_items(self, ingredient_ids: list[int], result_ids: list[int]) -> tuple[list[Ingredient], list[Result]]:
        """
        Fetches item data from the database, converts it to the appropriate
        entity types (Ingredient or Result), and caches ingredients for future use.

        Args:
            ingredient_ids (list[int]): List of item IDs for the recipe's ingredients.
            result_ids (list[int]): List of item IDs for the recipe's results.

        Returns:
            tuple[list[Ingredient], list[Result]]: A tuple containing two lists:
                - A list of Ingredient objects for the recipe's ingredients.
                - A list of Result objects for the recipe's results.
        """
        all_item_ids = ingredient_ids + result_ids
        all_item_models = self._item_repository.get_items(all_item_ids)

        ingredient_item_models = [item for item in all_item_models if item.item_id in ingredient_ids]
        result_item_models = [item for item in all_item_models if item.item_id in result_ids]

        ingredients = []
        with self._cache_lock:
            for item_model in ingredient_item_models:
                if item_model.item_id in self._ingredient_cache:
                    ingredients.append(self._ingredient_cache[item_model.item_id])
                else:
                    ingredient = self._convert_to_ingredient(item_model)
                    self._ingredient_cache[item_model.item_id] = ingredient
                    ingredients.append(ingredient)

        results = [self._convert_to_result(item) for item in result_item_models]

        return ingredients, results

    def _convert_to_ingredient(self, item_model: ItemModel) -> Ingredient:
        """
        Checks if the item is craftable and returns the appropriate
        ingredient type based on that information.

        Args:
            item_model (ItemModel): The ItemModel to convert.

        Returns:
            Ingredient or CraftableIngredient: The converted ingredient entity.
        """
        if self._recipe_repository.is_craftable(item_model.item_id):
            return CraftableIngredient(item_model.item_id, item_model.name, item_model.sort_name,
                                       item_model.stack_size)
        else:
            return Ingredient(item_model.item_id, item_model.name, item_model.sort_name, item_model.stack_size)

    def _convert_to_result(self, item_model: ItemModel) -> Result:
        """
        Convert an ItemModel to a Result entity.

        Args:
            item_model (ItemModel): The ItemModel to convert.

        Returns:
            Result: The converted result entity.
        """
        result = Result(item_model.item_id, item_model.name, item_model.sort_name, item_model.stack_size)
        return result

    def update_auction_data(self, item_id: int) -> None:
        """
        Fetches the latest auction data for the item and updates the
        corresponding Ingredient or Result entity with this information. All Result
        instances are synced with the new auction data.

        Args:
            item_id (int): The ID of the item to update auction data for.

        Raises:
            ValueError: If the item is not found in the ingredient cache or Result instances.
        """
        item = self._ingredient_cache.get(item_id)
        if not item:
            item = Result.get(item_id)

        if item:
            if (item.single_price is None or item.stack_price is None or
                    item.single_sell_freq is None or item.stack_sell_freq is None):
                auction_data = self._get_auction_data(item_id)

                item.single_price = auction_data[0]
                item.stack_price = auction_data[1]
                item.single_sell_freq = auction_data[2]
                item.stack_sell_freq = auction_data[3]
        else:
            raise ValueError(f"Item with id {item_id} not found in Ingredient cache or Result instances.")

        Result.sync(item)

    def update_vendor_cost(self, item_id: int) -> None:
        """
        Fetches the latest vendor cost for the item and updates the
        corresponding Ingredient entity with this information.

        Args:
            item_id (int): The ID of the item to update vendor cost for.

        Raises:
            ValueError: If the ingredient is not found in the cache.
        """
        ingredient = self._ingredient_cache.get(item_id)
        if ingredient:
            ingredient.vendor_cost = self._get_vendor_cost(item_id)
        else:
            raise ValueError(f"Ingredient with id {item_id} not found.")

    def update_guild_cost(self, item_id: int) -> None:
        """
        Fetches the latest guild cost for the item and updates the
        corresponding Ingredient entity with this information.

        Args:
            item_id (int): The ID of the item to update guild cost for.

        Raises:
            ValueError: If the ingredient is not found in the cache.
        """
        ingredient = self._ingredient_cache.get(item_id)
        if ingredient:
            ingredient.guild_cost = self._get_guild_cost(item_id)
        else:
            raise ValueError(f"Ingredient with id {item_id} not found.")

    def _get_auction_data(self, item_id: int) -> tuple[float | None, float | None, float | None, float | None]:
        """
        Retrieves the latest auction data from the AuctionController
        and formats it for use in updating item entities.

        Args:
            item_id (int): The ID of the item to fetch auction data for.

        Returns:
            tuple[float | None, float | None, float | None, float | None]: A tuple containing:
                - Single item price (float or None)
                - Stack price (float or None)
                - Single item sell frequency (float or None)
                - Stack sell frequency (float or None)
        """
        auction_items = self._auction_controller.get_auction_items_with_updates(item_id)
        single_price = None
        stack_price = None
        single_sell_freq = None
        stack_sell_freq = None

        for auction_item in auction_items:
            if not auction_item.is_stack:
                single_price = auction_item.avg_price if auction_item.avg_price > 0 else None
                single_sell_freq = auction_item.sell_freq if auction_item.sell_freq > 0 else None
            else:
                stack_price = auction_item.avg_price if auction_item.avg_price > 0 else None
                stack_sell_freq = auction_item.sell_freq if auction_item.sell_freq > 0 else None

        return single_price, stack_price, single_sell_freq, stack_sell_freq

    def _get_vendor_cost(self, item_id: int) -> int | None:
        """
        Retrieves vendor costs for the item, filters out vendors based on
        beastmen-controlled regions and conquest rankings, and returns the lowest available price.

        Args:
            item_id (int): The ID of the item to fetch vendor cost for.

        Returns:
            int | None: The lowest vendor cost for the item, or None if not available.
        """
        vendor_items = self._vendor_repository.get_vendor_items(item_id)

        filtered_vendor_items = self._filter_beastmen_controlled_vendors(vendor_items)
        filtered_vendor_items = self._filter_by_conquest_rank(filtered_vendor_items)

        prices = [vendor_item.price for vendor_item in filtered_vendor_items]

        return min(prices, default=None)

    def _filter_beastmen_controlled_vendors(self, vendor_items: list) -> list:
        """
        Checks each vendor item against the list of beastmen-controlled regions
        and removes those that are in such regions. Non-regional vendors are always included.

        Args:
            vendor_items (list): List of vendor items to filter.

        Returns:
            list: Filtered list of vendor items, excluding those in beastmen-controlled regions.
        """
        beastmen_regions = SettingsManager.get_beastmen_regions()
        filtered_items = []

        for vendor_item in vendor_items:
            regional_vendor = self._vendor_repository.get_regional_vendor(vendor_item.npc_id)
            if not regional_vendor:
                # Standard vendor, always include
                filtered_items.append(vendor_item)
            else:
                vendor_region = regional_vendor.region.lower()
                if vendor_region not in beastmen_regions:
                    filtered_items.append(vendor_item)

        return filtered_items

    def _filter_by_conquest_rank(self, vendor_items: list) -> list:
        """
        Checks each vendor item against the current conquest rankings
        and includes only those that are available based on the current ranks.
        Vendors with no rank requirement (rank 0) are always included.
        The ranking system is as follows:
        - 1: 1st rank (best)
        - 2: 2nd rank
        - 3: 3rd rank
        A lower number indicates a better rank.

        Args:
            vendor_items (list): List of vendor items to filter.

        Returns:
            list: Filtered list of vendor items, including only those that are available
                  given the current conquest rankings.
        """
        sandoria_rank = SettingsManager.get_sandoria_rank()
        bastok_rank = SettingsManager.get_bastok_rank()
        windurst_rank = SettingsManager.get_windurst_rank()

        filtered_items = []

        for vendor_item in vendor_items:
            if (vendor_item.sandoria_rank == 0 or vendor_item.sandoria_rank >= sandoria_rank) and \
               (vendor_item.bastok_rank == 0 or vendor_item.bastok_rank >= bastok_rank) and \
               (vendor_item.windurst_rank == 0 or vendor_item.windurst_rank >= windurst_rank):
                filtered_items.append(vendor_item)

        return filtered_items

    def _get_guild_cost(self, item_id: int) -> int | None:
        """
        Retrieves guild costs for the item from enabled guilds and
        returns the lowest available price.

        Args:
            item_id (int): The ID of the item to fetch guild cost for.

        Returns:
            int | None: The lowest guild cost for the item, or None if not available.


        """
        enabled_guilds = SettingsManager.get_enabled_guilds()
        guild_shops = self._guild_repository.get_guild_shops(item_id)
        prices = []

        for shop in guild_shops:
            if shop.initial_quantity > 0:
                guild_vendor = self._guild_repository.get_guild_vendor(shop.guild_id)
                if guild_vendor and guild_vendor.category in enabled_guilds:
                    prices.append(shop.min_price)

        return min(prices, default=None)
