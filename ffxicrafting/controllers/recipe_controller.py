from ..services import RecipeService


class RecipeController:
    @classmethod
    def get_recipe(cls, recipe_id):
        return RecipeService.get_recipe(recipe_id)

    @classmethod
    def get_recipes_by_level_generator(cls, *craft_levels):
        return RecipeService.get_recipes_by_level_generator(*craft_levels)

    @classmethod
    def search_recipe_generator(cls, search_term):
        return RecipeService.search_recipe_generator(search_term)

    @classmethod
    def clear_cache(cls):
        RecipeService.clear_cache()
