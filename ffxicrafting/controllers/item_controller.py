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
        Initialize the ItemController.

        Args:
            db (Database): The database connection object.

        Initializes repositories for items, recipes, vendors, and guilds,
        as well as the auction controller.
        """
        self._item_repository: ItemRepository = ItemRepository(db)
        self._recipe_repository: RecipeRepository = RecipeRepository(db)
        self._vendor_repository: VendorRepository = VendorRepository(db)
        self._guild_repository: GuildRepository = GuildRepository(db)
        self._auction_controller: AuctionController = AuctionController(db)

    def get_recipe_items(self, ingredient_ids: list[int], result_ids: list[int]) -> tuple[list[Ingredient], list[Result]]:
        """
        Fetch and convert items for a recipe's ingredients and results.

        Args:
            ingredient_ids (list[int]): List of item IDs for the recipe's ingredients.
            result_ids (list[int]): List of item IDs for the recipe's results.

        Returns:
            tuple[list[Ingredient], list[Result]]: A tuple containing two lists:
                - A list of Ingredient objects for the recipe's ingredients.
                - A list of Result objects for the recipe's results.

        This method fetches item data from the database, converts it to the appropriate
        entity types (Ingredient or Result), and caches ingredients for future use.
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
        Convert an ItemModel to an Ingredient or CraftableIngredient entity.

        Args:
            item_model (ItemModel): The ItemModel to convert.

        Returns:
            Ingredient or CraftableIngredient: The converted ingredient entity.

        This method checks if the item is craftable and returns the appropriate
        ingredient type based on that information.
        """
        if self._recipe_repository.is_craftable(item_model.item_id):
            return CraftableIngredient(item_model.item_id, item_model.sub_id, item_model.name,
                                       item_model.sort_name, item_model.stack_size, item_model.flags,
                                       item_model.ah, item_model.no_sale, item_model.base_sell)
        else:
            return Ingredient(item_model.item_id, item_model.sub_id, item_model.name,
                              item_model.sort_name, item_model.stack_size, item_model.flags,
                              item_model.ah, item_model.no_sale, item_model.base_sell)

    def _convert_to_result(self, item_model: ItemModel) -> Result:
        """
        Convert an ItemModel to a Result entity.

        Args:
            item_model (ItemModel): The ItemModel to convert.

        Returns:
            Result: The converted result entity.
        """
        result = Result(item_model.item_id, item_model.sub_id, item_model.name, item_model.sort_name,
                        item_model.stack_size, item_model.flags, item_model.ah, item_model.no_sale,
                        item_model.base_sell)
        return result

    def update_auction_data(self, item_id: int) -> None:
        """
        Update auction data for a specific item.

        Args:
            item_id (int): The ID of the item to update auction data for.

        Raises:
            ValueError: If the item is not found in the ingredient cache or Result instances.

        This method fetches the latest auction data for the item and updates the
        corresponding Ingredient or Result entity with this information. All Result
        instances are synced with the new auction data.
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
        Update vendor cost for a specific item.

        Args:
            item_id (int): The ID of the item to update vendor cost for.

        Raises:
            ValueError: If the ingredient is not found in the cache.

        This method fetches the latest vendor cost for the item and updates the
        corresponding Ingredient entity with this information.
        """
        ingredient = self._ingredient_cache.get(item_id)
        if ingredient:
            ingredient.vendor_cost = self._get_vendor_cost(item_id)
        else:
            raise ValueError(f"Ingredient with id {item_id} not found.")

    def update_guild_cost(self, item_id: int) -> None:
        """
        Update guild cost for a specific item.

        Args:
            item_id (int): The ID of the item to update guild cost for.

        Raises:
            ValueError: If the ingredient is not found in the cache.

        This method fetches the latest guild cost for the item and updates the
        corresponding Ingredient entity with this information.
        """
        ingredient = self._ingredient_cache.get(item_id)
        if ingredient:
            ingredient.guild_cost = self._get_guild_cost(item_id)
        else:
            raise ValueError(f"Ingredient with id {item_id} not found.")

    def _get_auction_data(self, item_id: int) -> tuple[float | None, float | None, float | None, float | None]:
        """
        Fetch auction data for a specific item.

        Args:
            item_id (int): The ID of the item to fetch auction data for.

        Returns:
            tuple[float | None, float | None, float | None, float | None]: A tuple containing:
                - Single item price (float or None)
                - Stack price (float or None)
                - Single item sell frequency (float or None)
                - Stack sell frequency (float or None)

        This method retrieves the latest auction data from the AuctionController
        and formats it for use in updating item entities.
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
        Fetch the vendor cost for a specific item.

        Args:
            item_id (int): The ID of the item to fetch vendor cost for.

        Returns:
            int | None: The lowest vendor cost for the item, or None if not available.

        This method retrieves vendor costs for the item, filters out vendors in
        Beastmen-controlled regions, and returns the lowest available price.
        """
        vendor_items = self._vendor_repository.get_vendor_items(item_id)
        beastmen_regions = SettingsManager.get_beastmen_regions()

        # Filter out regional vendors that are controlled by Beastmen
        filtered_vendor_items = []
        for vendor_item in vendor_items:
            regional_vendor = self._vendor_repository.get_regional_vendor(vendor_item.npc_id)
            if not regional_vendor:
                # Standard vendor
                filtered_vendor_items.append(vendor_item)
            else:
                vendor_region = regional_vendor.region.lower()
                if vendor_region not in beastmen_regions:
                    filtered_vendor_items.append(vendor_item)

        prices = [vendor_item.price for vendor_item in filtered_vendor_items]

        return min(prices, default=None)

    def _get_guild_cost(self, item_id: int) -> int | None:
        """
        Fetch the guild cost for a specific item.

        Args:
            item_id (int): The ID of the item to fetch guild cost for.

        Returns:
            int | None: The lowest guild cost for the item, or None if not available.

        This method retrieves guild costs for the item from enabled guilds and
        returns the lowest available price.
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
