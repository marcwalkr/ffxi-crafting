from database import Database
from entities import Recipe
from services import ItemService


class RecipeService:
    db = Database()

    _cache = {
        "get_recipe": {},
        "get_recipes_by_level_generator": {},
        "search_recipe_generator": {}
    }

    @classmethod
    def get_recipe(cls, recipe_id):
        if recipe_id in cls._cache["get_recipe"]:
            return cls._cache["get_recipe"][recipe_id]
        else:
            recipe_tuple = cls.db.get_recipe(recipe_id)
            if recipe_tuple is not None:
                crystal_id = recipe_tuple[11]
                hq_crystal_id = recipe_tuple[12]
                ingredient_ids = recipe_tuple[13:21]
                result_ids = recipe_tuple[21:25]
                result_quantities = recipe_tuple[25:29]
                result_name = recipe_tuple[29]

                all_item_ids = [crystal_id] + list(ingredient_ids) + list(result_ids)
                all_items = ItemService.get_items(tuple(all_item_ids))

                crystal = next(item for item in all_items if item.item_id == crystal_id)
                ingredients = [item for item in all_items if item.item_id in ingredient_ids]
                results = [item for item in all_items if item.item_id in result_ids]

                recipe = Recipe(
                    *recipe_tuple[:11],
                    crystal_id,
                    hq_crystal_id,
                    *ingredient_ids,
                    *result_ids,
                    *result_quantities,
                    result_name,
                    crystal,
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
                cls._cache["get_recipe"][recipe_id] = recipe
                return recipe
            else:
                return None

    @classmethod
    def get_recipes_by_level_generator(cls, *craft_levels):
        cache_key = tuple(craft_levels)
        if cache_key in cls._cache["get_recipes_by_level_generator"]:
            for recipe in cls._cache["get_recipes_by_level_generator"][cache_key]:
                yield recipe
        else:
            results = list(cls.db.get_recipes_by_level_generator(*craft_levels))
            recipes = []
            for recipe_tuple in results:
                crystal_id = recipe_tuple[11]
                hq_crystal_id = recipe_tuple[12]
                ingredient_ids = recipe_tuple[13:21]
                result_ids = recipe_tuple[21:25]
                result_quantities = recipe_tuple[25:29]
                result_name = recipe_tuple[29]

                all_item_ids = [crystal_id] + list(ingredient_ids) + list(result_ids)
                all_items = ItemService.get_items(tuple(all_item_ids))

                crystal = next(item for item in all_items if item.item_id == crystal_id)
                ingredients = [item for item in all_items if item.item_id in ingredient_ids]
                results = [item for item in all_items if item.item_id in result_ids]

                recipe = Recipe(
                    *recipe_tuple[:11],
                    crystal_id,
                    hq_crystal_id,
                    *ingredient_ids,
                    *result_ids,
                    *result_quantities,
                    result_name,
                    crystal,
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
                yield recipe
            cls._cache["get_recipes_by_level_generator"][cache_key] = recipes

    @classmethod
    def search_recipe_generator(cls, search_term):
        if search_term in cls._cache["search_recipe_generator"]:
            for recipe in cls._cache["search_recipe_generator"][search_term]:
                yield recipe
        else:
            results = cls.db.search_recipe_generator(search_term)
            recipes = []
            for recipe_tuple in results:
                crystal_id = recipe_tuple[11]
                hq_crystal_id = recipe_tuple[12]
                ingredient_ids = recipe_tuple[13:21]
                result_ids = recipe_tuple[21:25]
                result_quantities = recipe_tuple[25:29]
                result_name = recipe_tuple[29]

                all_item_ids = [crystal_id] + list(ingredient_ids) + list(result_ids)
                all_items = ItemService.get_items(tuple(all_item_ids))

                crystal = next(item for item in all_items if item.item_id == crystal_id)
                ingredients = [item for item in all_items if item.item_id in ingredient_ids]
                results = [item for item in all_items if item.item_id in result_ids]

                recipe = Recipe(
                    *recipe_tuple[:11],
                    crystal_id,
                    hq_crystal_id,
                    *ingredient_ids,
                    *result_ids,
                    *result_quantities,
                    result_name,
                    crystal,
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
                yield recipe
            cls._cache["search_recipe_generator"][search_term] = recipes

    @classmethod
    def clear_cache(cls):
        cls._cache = {
            "get_recipe": {},
            "get_recipes_by_level_generator": {},
            "search_recipe_generator": {}
        }
