from entities import Recipe
from utils import unique_preserve_order
from database import Database
from controllers import ItemController


class RecipeController:
    cache = {
        "get_recipes_by_level": {},
        "search_recipe": {}
    }
    result_item_ids = None

    def __init__(self) -> None:
        self.db = Database()
        self.item_controller = ItemController(self.db)

    def get_recipe(self, recipe_id):
        for cache_name in self.cache:
            for recipes in self.cache[cache_name].values():
                for recipe in recipes:
                    if recipe.id == recipe_id:
                        return recipe
        raise ValueError(f"Recipe with id {recipe_id} not found in cache.")

    def get_recipes_by_level(self, *craft_levels, batch_size, offset):
        cache_key = (craft_levels, offset)
        if cache_key in self.cache["get_recipes_by_level"]:
            return self.cache["get_recipes_by_level"][cache_key]
        else:
            results = list(self.db.get_recipes_by_level(*craft_levels, batch_size, offset))
            if results:
                recipe_items = self.get_recipe_items(results)
                recipes = self.create_recipe_objects(results, recipe_items)
                self.cache["get_recipes_by_level"][cache_key] = recipes
                return recipes
            else:
                return []

    def search_recipe(self, search_term, batch_size, offset):
        cache_key = (search_term, offset)
        if cache_key in self.cache["search_recipe"]:
            return self.cache["search_recipe"][cache_key]
        else:
            results = self.db.search_recipe(search_term, batch_size, offset)
            if results:
                recipe_items = self.get_recipe_items(results)
                recipes = self.create_recipe_objects(results, recipe_items)
                self.cache["search_recipe"][cache_key] = recipes
                return recipes
            else:
                return []

    def get_recipe_items(self, recipe_tuples):
        all_crystal_ids = []
        all_ingredient_ids = []
        all_result_ids = []
        for recipe_tuple in recipe_tuples:
            all_crystal_ids.append(recipe_tuple[11])
            all_ingredient_ids.extend(recipe_tuple[13:21])
            all_result_ids.extend(recipe_tuple[21:25])
    
        unique_item_ids = unique_preserve_order(all_crystal_ids + all_ingredient_ids + all_result_ids)
        return self.item_controller.get_items(unique_item_ids)

    def create_recipe_objects(self, recipe_tuples, unique_items):
        recipes = []
        for recipe_tuple in recipe_tuples:
            crystal_id = recipe_tuple[11]
            hq_crystal_id = recipe_tuple[12]
            ingredient_ids = recipe_tuple[13:21]
            result_ids = recipe_tuple[21:25]
            result_quantities = recipe_tuple[25:29]
            result_name = recipe_tuple[29]

            crystal = next(item for item in unique_items if item.item_id == crystal_id)
            ingredient_items = [item for item in unique_items if item.item_id in ingredient_ids]
            result_items = [item for item in unique_items if item.item_id in result_ids]

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

            recipes.append(recipe)
        return recipes

    def is_ingredient_craftable(self, item_id):
        if self.result_item_ids is None:
            self.result_item_ids = self.db.get_all_result_item_ids()
        return item_id in self.result_item_ids
