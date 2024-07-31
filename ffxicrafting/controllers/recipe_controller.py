import logging
from entities import Recipe
from controllers import ItemController

logger = logging.getLogger(__name__)


class RecipeController:
    query_cache = {
        "get_recipes_by_level": {},
        "search_recipe": {}
    }
    recipe_cache = {}
    all_result_item_ids = None

    def __init__(self, db) -> None:
        self.db = db
        self.item_controller = ItemController(self.db)

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
        recipes = self.process_and_cache_recipes(recipe_tuples)
        self.query_cache["get_recipes_by_level"][cache_key] = recipes
        return recipes

    def search_recipe(self, search_term, batch_size, offset):
        cache_key = (search_term, batch_size, offset)
        if cache_key in self.query_cache["search_recipe"]:
            return self.query_cache["search_recipe"][cache_key]

        recipe_tuples = self.db.search_recipe(search_term, batch_size, offset)
        recipes = self.process_and_cache_recipes(recipe_tuples)
        self.query_cache["search_recipe"][cache_key] = recipes
        return recipes

    def process_and_cache_recipes(self, recipe_tuples):
        all_item_ids = set()
        for recipe_tuple in recipe_tuples:
            all_item_ids.add(recipe_tuple[11])  # crystal
            all_item_ids.update(recipe_tuple[13:21])  # ingredients
            all_item_ids.update(recipe_tuple[21:25])  # results

        all_items = {item.item_id: item for item in self.item_controller.get_items(list(all_item_ids))}

        recipes = []
        for recipe_tuple in recipe_tuples:
            recipe_id = recipe_tuple[0]
            if recipe_id in self.recipe_cache:
                recipes.append(self.recipe_cache[recipe_id])
            else:
                recipe = self.create_recipe_object(recipe_tuple, all_items)
                self.recipe_cache[recipe_id] = recipe
                recipes.append(recipe)
        return recipes

    def create_recipe_object(self, recipe_tuple, all_items):
        crystal_id = recipe_tuple[11]
        hq_crystal_id = recipe_tuple[12]
        ingredient_ids = recipe_tuple[13:21]
        result_ids = recipe_tuple[21:25]
        result_quantities = recipe_tuple[25:29]
        result_name = recipe_tuple[29]

        crystal = all_items[crystal_id]
        ingredient_items = [all_items[item_id] for item_id in ingredient_ids if item_id > 0]
        result_items = [all_items[item_id] for item_id in result_ids if item_id > 0]

        # Treat the crystal as an ingredient
        ingredient_items.insert(0, crystal)

        # Convert ingredient Item objects into Ingredient objects
        ingredients = []
        for ingredient_item in ingredient_items:
            craftable = self.is_ingredient_craftable(ingredient_item.item_id)
            ingredient = self.item_controller.convert_to_ingredient(ingredient_item, craftable)
            ingredients.append(ingredient)

        # Convert result Item objects into Result objects
        results = [self.item_controller.convert_to_result(result) for result in result_items]

        recipe = Recipe(
            *recipe_tuple[:11],
            crystal_id,
            hq_crystal_id,
            *ingredient_ids,
            *result_ids,
            *result_quantities,
            result_name,
            ingredients[0],  # crystal
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

    def get_all_result_item_ids(self):
        if self.all_result_item_ids is None:
            self.all_result_item_ids = self.db.get_all_result_item_ids()
        return self.all_result_item_ids

    def is_ingredient_craftable(self, item_id):
        return item_id in self.get_all_result_item_ids()
