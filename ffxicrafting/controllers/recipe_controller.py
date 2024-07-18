from services import RecipeService


class RecipeController:
    @classmethod
    def get_recipe(cls, recipe_id):
        return RecipeService.get_recipe(recipe_id)

    @classmethod
    def get_recipes_by_level(cls, *craft_levels, batch_size, offset):
        return RecipeService.get_recipes_by_level(*craft_levels, batch_size=batch_size, offset=offset)

    @classmethod
    def search_recipe(cls, search_term, batch_size, offset):
        return RecipeService.search_recipe(search_term, batch_size, offset)
