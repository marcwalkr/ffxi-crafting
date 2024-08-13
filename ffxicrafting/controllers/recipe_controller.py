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

    _cache = []

    def __init__(self, db: Database) -> None:
        """
        Initialize the RecipeController with database connection and required controllers.
        All Recipe objects are created and cached on initialization.

        Args:
            db (Database): The database connection object.
        """
        self._item_controller: ItemController = ItemController(db)
        self._recipe_repository: RecipeRepository = RecipeRepository(db)
        if not RecipeController._cache:
            self._create_recipe_objects()

    def _create_recipe_objects(self) -> None:
        """
        Load all recipes into the cache.
        """
        recipe_models = self._recipe_repository.get_all_recipes()
        recipes = self._process_recipe_models(recipe_models)
        RecipeController._cache = recipes
        self._recipe_repository.delete_cache()

    def search_recipe(self, search_term: str) -> list[Recipe]:
        """
        Search for recipes in the cache based on a search term.
        Searches through the recipe's result items.

        Args:
            search_term (str): The term to search for in recipe result items.

        Returns:
            list[Recipe]: A list of Recipe objects matching the search term.
        """
        recipes = []
        for recipe in self._cache:
            for result in recipe.get_unique_results():
                if search_term.lower() in result.get_formatted_name().lower():
                    if recipe not in recipes:
                        recipes.append(recipe)
        return recipes

    def _process_recipe_models(self, recipe_models: list[RecipeModel]) -> list[Recipe]:
        """
        Process a list of RecipeModel objects into Recipe objects.

        Args:
            recipe_models (list[RecipeModel]): A list of RecipeModel objects to process.

        Returns:
            list[Recipe]: A list of processed Recipe objects.
        """
        recipes = []
        for recipe_model in recipe_models:
            item_ids = set()
            item_ids.update([recipe_model.crystal, recipe_model.ingredient1, recipe_model.ingredient2,
                             recipe_model.ingredient3, recipe_model.ingredient4, recipe_model.ingredient5,
                             recipe_model.ingredient6, recipe_model.ingredient7, recipe_model.ingredient8,
                             recipe_model.result, recipe_model.result_hq1, recipe_model.result_hq2,
                             recipe_model.result_hq3])

            # Remove empty ingredients represented by 0
            item_ids.discard(0)

            items = self._item_controller.get_recipe_items(list(item_ids))

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
            recipes.append(recipe)

        return recipes

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
