from entities import Recipe
from services import ItemService
from utils import unique_preserve_order


class RecipeService:
    _cache = {
        "get_recipes_by_level": {},
        "search_recipe": {}
    }

    def __init__(self, db) -> None:
        self.db = db
        self.item_service = ItemService(self.db)

    def get_recipe(self, recipe_id):
        for cache_name in self._cache:
            for recipes in self._cache[cache_name].values():
                for recipe in recipes:
                    if recipe.id == recipe_id:
                        return recipe
        raise ValueError(f"Recipe with id {recipe_id} not found in cache.")

    def get_recipes_by_level(self, *craft_levels, batch_size, offset):
        cache_key = (craft_levels, offset)
        if cache_key in self._cache["get_recipes_by_level"]:
            return self._cache["get_recipes_by_level"][cache_key]
        else:
            results = list(self.db.get_recipes_by_level(*craft_levels, batch_size, offset))
            if results:
                recipe_items = self._get_recipe_items(results)
                recipes = self._create_recipe_objects(results, recipe_items)
                self._cache["get_recipes_by_level"][cache_key] = recipes
                return recipes
            else:
                return []

    def search_recipe(self, search_term, batch_size, offset):
        cache_key = (search_term, offset)
        if cache_key in self._cache["search_recipe"]:
            return self._cache["search_recipe"][cache_key]
        else:
            results = self.db.search_recipe(search_term, batch_size, offset)
            if results:
                recipe_items = self._get_recipe_items(results)
                recipes = self._create_recipe_objects(results, recipe_items)
                self._cache["search_recipe"][cache_key] = recipes
                return recipes
            else:
                return []

    def _get_recipe_items(self, recipe_tuples):
        all_crystal_ids = []
        all_ingredient_ids = []
        all_result_ids = []
        for recipe_tuple in recipe_tuples:
            all_crystal_ids.append(recipe_tuple[11])
            all_ingredient_ids.extend(recipe_tuple[13:21])
            all_result_ids.extend(recipe_tuple[21:25])

        unique_item_ids = unique_preserve_order(all_crystal_ids + all_ingredient_ids + all_result_ids)
        return self.item_service.get_items(unique_item_ids)

    def _create_recipe_objects(self, recipe_tuples, unique_items):
        recipes = []
        for recipe_tuple in recipe_tuples:
            crystal_id = recipe_tuple[11]
            hq_crystal_id = recipe_tuple[12]
            ingredient_ids = recipe_tuple[13:21]
            result_ids = recipe_tuple[21:25]
            result_quantities = recipe_tuple[25:29]
            result_name = recipe_tuple[29]

            crystal = next(item for item in unique_items if item.item_id == crystal_id)
            ingredients = [item for item in unique_items if item.item_id in ingredient_ids]
            results = [item for item in unique_items if item.item_id in result_ids]

            # Treat the crystal as an ingredient
            ingredients.insert(0, crystal)

            # Convert ingredient Item objects into Ingredient objects
            ingredients = [self.item_service.convert_to_ingredient(ingredient) for ingredient in ingredients]

            # Convert result Item objects into Result objects
            results = [self.item_service.convert_to_result(result) for result in results]

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
