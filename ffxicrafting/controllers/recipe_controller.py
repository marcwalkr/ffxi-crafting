import logging
from entities import Recipe
from repositories import RecipeRepository
from controllers import ItemController

logger = logging.getLogger(__name__)


class RecipeController:
    query_cache = {
        "get_recipes_by_level": {},
        "search_recipe": {}
    }
    recipe_cache = {}

    def __init__(self, db) -> None:
        self.db = db
        self.item_controller = ItemController(self.db)
        self.recipe_repository = RecipeRepository(self.db)

    def get_recipe(self, recipe_id):
        if recipe_id in self.recipe_cache:
            return self.recipe_cache[recipe_id]
        else:
            raise ValueError(f"Recipe with id {recipe_id} not found in cache.")

    def get_recipes_by_level(self, *craft_levels, batch_size, offset):
        cache_key = (craft_levels, batch_size, offset)
        if cache_key in self.query_cache["get_recipes_by_level"]:
            return self.query_cache["get_recipes_by_level"][cache_key]

        recipe_tuples = self.db.get_recipes_by_level(*craft_levels, batch_size, offset)
        if recipe_tuples:
            recipes = self.process_and_cache_recipes(recipe_tuples)
            self.query_cache["get_recipes_by_level"][cache_key] = recipes
            return recipes
        else:
            return []

    def search_recipe(self, search_term, batch_size, offset):
        cache_key = (search_term, batch_size, offset)
        if cache_key in self.query_cache["search_recipe"]:
            return self.query_cache["search_recipe"][cache_key]

        recipe_tuples = self.db.search_recipe(search_term, batch_size, offset)
        if recipe_tuples:
            recipes = self.process_and_cache_recipes(recipe_tuples)
            self.query_cache["search_recipe"][cache_key] = recipes
            return recipes
        else:
            return []

    def process_and_cache_recipes(self, recipe_tuples):
        ingredient_item_ids = set()
        result_item_ids = set()

        for recipe_tuple in recipe_tuples:
            # Treat the crystal as an ingredient
            ingredient_item_ids.add(recipe_tuple[11])

            # Gather ingredient ids, excluding empty ingredients represented by 0
            ingredient_item_ids.update(id for id in recipe_tuple[13:21] if id != 0)

            # Gather result ids
            result_item_ids.update(recipe_tuple[21:25])

        ingredients, results = self.item_controller.get_recipe_items(list(ingredient_item_ids), list(result_item_ids))

        recipes = []
        for recipe_tuple in recipe_tuples:
            recipe_id = recipe_tuple[0]
            if recipe_id in self.recipe_cache:
                recipes.append(self.recipe_cache[recipe_id])
            else:
                recipe = self.create_recipe_object(recipe_tuple, ingredients, results)
                self.recipe_cache[recipe_id] = recipe
                recipes.append(recipe)
        return recipes

    def create_recipe_object(self, recipe_tuple, ingredients, results):
        crystal_id = recipe_tuple[11]
        hq_crystal_id = recipe_tuple[12]
        ingredient_ids = recipe_tuple[13:21]
        result_ids = recipe_tuple[21:25]
        result_quantities = recipe_tuple[25:29]
        result_name = recipe_tuple[29]

        recipe = Recipe(
            *recipe_tuple[:11],
            crystal_id,
            hq_crystal_id,
            *ingredient_ids,
            *result_ids,
            *result_quantities,
            result_name,
            next((ingredient for ingredient in ingredients if ingredient.item_id == crystal_id), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == ingredient_ids[0]), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == ingredient_ids[1]), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == ingredient_ids[2]), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == ingredient_ids[3]), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == ingredient_ids[4]), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == ingredient_ids[5]), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == ingredient_ids[6]), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == ingredient_ids[7]), None),
            next((result for result in results if result.item_id == result_ids[0]), None),
            next((result for result in results if result.item_id == result_ids[1]), None),
            next((result for result in results if result.item_id == result_ids[2]), None),
            next((result for result in results if result.item_id == result_ids[3]), None)
        )
        return recipe
