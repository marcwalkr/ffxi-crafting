from database import Database
from models import RecipeModel


class RecipeRepository:
    """
    Repository class for handling recipe-related data operations.

    This class provides methods to interact with the database for retrieving
    recipe information. It implements caching to improve performance for
    frequently accessed queries.
    """

    _query_cache: dict[str, dict[tuple, list[RecipeModel]]] = {
        "get_recipes_by_level": {},
        "search_recipe": {}
    }
    _all_result_item_ids: list[int] | None = None

    def __init__(self, db: Database) -> None:
        """
        Initialize a RecipeRepository instance.

        Args:
            db (Database): The database connection object used for querying recipe data.
        """
        self._db = db

    def get_recipes_by_level(self, *craft_levels: int, batch_size: int, offset: int) -> list[RecipeModel]:
        """
        Retrieve recipes based on crafting levels, with pagination.

        This method first checks the cache for the requested query. If not found,
        it queries the database and caches the result for future use.

        Args:
            *craft_levels (int): Variable number of crafting level arguments.
            batch_size (int): The number of recipes to retrieve per batch.
            offset (int): The offset for pagination.

        Returns:
            list[RecipeModel]: A list of RecipeModel objects matching the criteria.
        """
        cache_key = (craft_levels, batch_size, offset)
        if cache_key in self._query_cache["get_recipes_by_level"]:
            return self._query_cache["get_recipes_by_level"][cache_key]

        recipe_tuples = self._db.get_recipes_by_level(*craft_levels, batch_size, offset)
        return self._cache_and_return_recipes(recipe_tuples, cache_key, "get_recipes_by_level")

    def search_recipe(self, search_term: str, batch_size: int, offset: int) -> list[RecipeModel]:
        """
        Search for recipes based on a search term, with pagination.

        This method first checks the cache for the requested query. If not found,
        it queries the database and caches the result for future use.

        Args:
            search_term (str): The term to search for in recipe results.
            batch_size (int): The number of recipes to retrieve per batch.
            offset (int): The offset for pagination.

        Returns:
            list[RecipeModel]: A list of RecipeModel objects matching the search criteria.
        """
        cache_key = (search_term, batch_size, offset)
        if cache_key in self._query_cache["search_recipe"]:
            return self._query_cache["search_recipe"][cache_key]

        recipe_tuples = self._db.search_recipe(search_term, batch_size, offset)
        return self._cache_and_return_recipes(recipe_tuples, cache_key, "search_recipe")

    def is_craftable(self, item_id: int) -> bool:
        """
        Check if an item is craftable (i.e., is the result of any recipe).

        This method uses a cached list of all craftable item IDs for efficient lookup.

        Args:
            item_id (int): The ID of the item to check.

        Returns:
            bool: True if the item is craftable, False otherwise.
        """
        return item_id in self._get_all_result_item_ids()

    def _cache_and_return_recipes(self, recipe_tuples: list[tuple], cache_key: tuple,
                                  cache_name: str) -> list[RecipeModel]:
        """
        Cache the recipe query results and return RecipeModel objects.

        This is a helper method used by get_recipes_by_level and search_recipe.

        Args:
            recipe_tuples (list[tuple]): The raw recipe data from the database.
            cache_key (tuple): The key to use for caching the results.
            cache_name (str): The name of the cache to use ("get_recipes_by_level" or "search_recipe").

        Returns:
            list[RecipeModel]: A list of RecipeModel objects created from the recipe tuples.
        """
        if recipe_tuples:
            recipe_models = [RecipeModel(*recipe_tuple) for recipe_tuple in recipe_tuples]
            self._query_cache[cache_name][cache_key] = recipe_models
            return recipe_models
        else:
            return []

    def _get_all_result_item_ids(self) -> list[int]:
        """
        Retrieve and cache a list of all item IDs that are results of recipes.

        This method is used by is_craftable for efficient lookups.

        Returns:
            list[int]: A list of all item IDs that are results of recipes.
        """
        if self._all_result_item_ids is None:
            self._all_result_item_ids = self._db.get_all_result_item_ids()
        return self._all_result_item_ids
