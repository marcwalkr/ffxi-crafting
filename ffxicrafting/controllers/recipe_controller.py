import logging
from database import Database
from entities import Recipe, Item
from models import RecipeModel
from repositories import RecipeRepository
from controllers import ItemController

logger = logging.getLogger(__name__)


class RecipeController:
    """
    Controller class for managing recipe-related operations.
    """

    _recipe_cache = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize the RecipeController with database connection and required controllers.

        Args:
            db (Database): The database connection object.
        """
        self._item_controller: ItemController = ItemController(db)
        self._recipe_repository: RecipeRepository = RecipeRepository(db)

    def get_recipe(self, recipe_id: int) -> Recipe:
        """
        Retrieve a recipe from the cache by its ID.

        Args:
            recipe_id (int): The ID of the recipe to retrieve.

        Returns:
            Recipe: The requested recipe object.

        Raises:
            ValueError: If the recipe with the given ID is not found in the cache.
        """
        if recipe_id in self._recipe_cache:
            return self._recipe_cache[recipe_id]
        else:
            raise ValueError(f"Recipe with id {recipe_id} not found in cache.")

    def get_recipes_by_level(self, *craft_levels: int, batch_size: int, offset: int) -> list[Recipe]:
        """
        Retrieve recipes based on craft levels, with pagination support.

        Args:
            *craft_levels (int): Variable number of craft levels to filter recipes by.
            batch_size (int): The number of recipes to retrieve in this batch.
            offset (int): The offset from which to start retrieving recipes.

        Returns:
            list[Recipe]: A list of Recipe objects matching the specified criteria.
        """
        recipe_models = self._recipe_repository.get_recipes_by_level(
            *craft_levels, batch_size=batch_size, offset=offset)
        if recipe_models:
            recipes = self._process_and_cache_recipes(recipe_models)
            self._recipe_cache.update({recipe.id: recipe for recipe in recipes})
            return recipes
        else:
            return []

    def search_recipe(self, search_term: str, batch_size: int, offset: int) -> list[Recipe]:
        """
        Search for recipes based on a search term, with pagination support.

        Args:
            search_term (str): The term to search for in recipe names or ingredients.
            batch_size (int): The number of recipes to retrieve in this batch.
            offset (int): The offset from which to start retrieving recipes.

        Returns:
            list[Recipe]: A list of Recipe objects matching the search term.
        """
        recipe_models = self._recipe_repository.search_recipe(search_term, batch_size, offset)
        if recipe_models:
            recipes = self._process_and_cache_recipes(recipe_models)
            self._recipe_cache.update({recipe.id: recipe for recipe in recipes})
            return recipes
        else:
            return []

    def _process_and_cache_recipes(self, recipe_models: list[RecipeModel]) -> list[Recipe]:
        """
        Process a list of RecipeModel objects into Recipe objects and cache them.

        Args:
            recipe_models (list[RecipeModel]): A list of RecipeModel objects to process.

        Returns:
            list[Recipe]: A list of processed Recipe objects.
        """
        recipes = []
        for recipe_model in recipe_models:
            if recipe_model.id in self._recipe_cache:
                recipes.append(self._recipe_cache[recipe_model.id])
                continue

            item_ids = set()

            item_ids.update([recipe_model.crystal, recipe_model.ingredient1, recipe_model.ingredient2,
                             recipe_model.ingredient3, recipe_model.ingredient4, recipe_model.ingredient5,
                             recipe_model.ingredient6, recipe_model.ingredient7, recipe_model.ingredient8,
                             recipe_model.result, recipe_model.result_hq1, recipe_model.result_hq2,
                             recipe_model.result_hq3])

            # Remove empty ingredients represented by 0
            item_ids.discard(0)

            items = self._item_controller.get_recipe_items(list(item_ids))
            self._set_costs(items)

            crystal = next((item for item in items if item.item_id == recipe_model.crystal), None)
            ingredient1 = next((item for item in items if item.item_id == recipe_model.ingredient1), None)
            ingredient2 = next((item for item in items if item.item_id == recipe_model.ingredient2), None)
            ingredient3 = next((item for item in items if item.item_id == recipe_model.ingredient3), None)
            ingredient4 = next((item for item in items if item.item_id == recipe_model.ingredient4), None)
            ingredient5 = next((item for item in items if item.item_id == recipe_model.ingredient5), None)
            ingredient6 = next((item for item in items if item.item_id == recipe_model.ingredient6), None)
            ingredient7 = next((item for item in items if item.item_id == recipe_model.ingredient7), None)
            ingredient8 = next((item for item in items if item.item_id == recipe_model.ingredient8), None)
            ingredients = [crystal, ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6,
                           ingredient7, ingredient8]

            result = next((item for item in items if item.item_id == recipe_model.result), None)
            result_hq1 = next((item for item in items if item.item_id == recipe_model.result_hq1), None)
            result_hq2 = next((item for item in items if item.item_id == recipe_model.result_hq2), None)
            result_hq3 = next((item for item in items if item.item_id == recipe_model.result_hq3), None)
            results = [result, result_hq1, result_hq2, result_hq3]

            recipe = self._create_recipe_object(recipe_model, ingredients, results)
            self._recipe_cache[recipe_model.id] = recipe
            recipes.append(recipe)

        return recipes

    def _set_costs(self, items: list[Item]) -> None:
        """
        Update the costs of ingredients used in the recipe.

        Args:
            items (list[Item]): A list of items to update the costs for.
        """
        for item in items:
            self._item_controller.update_vendor_cost(item.item_id)
            self._item_controller.update_guild_cost(item.item_id)
            self._item_controller.update_auction_data(item.item_id)

    def _create_recipe_object(self, recipe_model: RecipeModel, ingredients: list[Item], results: list[Item]) -> Recipe:
        """
        Create a Recipe object from a RecipeModel and lists of ingredients and results.

        Args:
            recipe_model (RecipeModel): The RecipeModel to convert into a Recipe object.
            ingredients (list[Item]): A list of all unique ingredients for the recipe.
            results (list[Item]): A list of all unique results for the recipe.

        Returns:
            Recipe: A fully populated Recipe object.
        """
        recipe = Recipe(
            recipe_model.id, recipe_model.desynth, recipe_model.key_item, recipe_model.wood, recipe_model.smith,
            recipe_model.gold, recipe_model.cloth, recipe_model.leather, recipe_model.bone, recipe_model.alchemy,
            recipe_model.cook, recipe_model.crystal, recipe_model.ingredient1, recipe_model.ingredient2,
            recipe_model.ingredient3, recipe_model.ingredient4, recipe_model.ingredient5, recipe_model.ingredient6,
            recipe_model.ingredient7, recipe_model.ingredient8, recipe_model.result, recipe_model.result_hq1,
            recipe_model.result_hq2, recipe_model.result_hq3, recipe_model.result_qty, recipe_model.result_hq1_qty,
            recipe_model.result_hq2_qty, recipe_model.result_hq3_qty, recipe_model.result_name,
            ingredient_objects=ingredients,
            result_objects=results
        )
        return recipe
