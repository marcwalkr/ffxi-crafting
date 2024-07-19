from services import RecipeService


class RecipeController:
    def __init__(self, db) -> None:
        self.recipe_service = RecipeService(db)

    def get_recipe(self, recipe_id):
        return self.recipe_service.get_recipe(recipe_id)

    def get_recipes_by_level(self, *craft_levels, batch_size, offset):
        return self.recipe_service.get_recipes_by_level(*craft_levels, batch_size=batch_size, offset=offset)

    def search_recipe(self, search_term, batch_size, offset):
        return self.recipe_service.search_recipe(search_term, batch_size, offset)
