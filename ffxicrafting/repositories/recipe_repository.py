from models import RecipeModel


class RecipeRepository:
    query_cache = {
        "get_recipes_by_level": {},
        "search_recipe": {}
    }
    all_result_item_ids = None

    def __init__(self, db):
        self.db = db

    def get_recipes_by_level(self, *craft_levels, batch_size, offset):
        cache_key = (craft_levels, batch_size, offset)
        if cache_key in self.query_cache["get_recipes_by_level"]:
            return self.query_cache["get_recipes_by_level"][cache_key]

        recipe_tuples = self.db.get_recipes_by_level(*craft_levels, batch_size, offset)
        return self.cache_and_return_recipes(recipe_tuples, cache_key, "get_recipes_by_level")

    def search_recipe(self, search_term, batch_size, offset):
        cache_key = (search_term, batch_size, offset)
        if cache_key in self.query_cache["search_recipe"]:
            return self.query_cache["search_recipe"][cache_key]

        recipe_tuples = self.db.search_recipe(search_term, batch_size, offset)
        return self.cache_and_return_recipes(recipe_tuples, cache_key, "search_recipe")

    def cache_and_return_recipes(self, recipe_tuples, cache_key, cache_name):
        if recipe_tuples:
            recipe_models = [RecipeModel(*recipe_tuple) for recipe_tuple in recipe_tuples]
            self.query_cache[cache_name][cache_key] = recipe_models
            return recipe_models
        else:
            return []

    def get_all_result_item_ids(self):
        if self.all_result_item_ids is None:
            self.all_result_item_ids = self.db.get_all_result_item_ids()
        return self.all_result_item_ids

    def is_craftable(self, item_id):
        return item_id in self.get_all_result_item_ids()
