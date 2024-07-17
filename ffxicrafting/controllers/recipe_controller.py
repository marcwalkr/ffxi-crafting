from database.database import Database
from entities.recipe import Recipe


class RecipeController:
    db = Database()

    _cache = {
        'get_recipe': {},
        'get_recipes_by_level_generator': {},
        'search_recipe_generator': {}
    }

    @classmethod
    def get_recipe(cls, recipe_id):
        if recipe_id in cls._cache['get_recipe']:

            return Recipe(*cls._cache['get_recipe'][recipe_id])
        else:
            recipe_tuple = cls.db.get_recipe(recipe_id)
            if recipe_tuple is not None:
                cls._cache['get_recipe'][recipe_id] = recipe_tuple
                return Recipe(*recipe_tuple)
            else:
                return None

    @classmethod
    def get_recipes_by_level_generator(cls, *craft_levels):
        cache_key = tuple(craft_levels)
        if cache_key in cls._cache['get_recipes_by_level_generator']:
            for recipe_tuple in cls._cache['get_recipes_by_level_generator'][cache_key]:
                yield Recipe(*recipe_tuple)
        else:
            results = list(cls.db.get_recipes_by_level_generator(*craft_levels))
            cls._cache['get_recipes_by_level_generator'][cache_key] = results
            for recipe_tuple in results:
                yield Recipe(*recipe_tuple)

    @classmethod
    def search_recipe_generator(cls, search_term):
        if search_term in cls._cache['search_recipe_generator']:
            for recipe_tuple in cls._cache['search_recipe_generator'][search_term]:
                yield Recipe(*recipe_tuple)
        else:
            results = list(cls.db.search_recipe_generator(search_term))
            cls._cache['search_recipe_generator'][search_term] = results
            for recipe_tuple in results:
                yield Recipe(*recipe_tuple)

    @classmethod
    def clear_cache(cls):
        cls._cache = {
            'get_recipe': {},
            'get_recipes_by_level_generator': {},
            'search_recipe_generator': {}
        }
