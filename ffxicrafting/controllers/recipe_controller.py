from database.database import Database
from entities.recipe import Recipe


class RecipeController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_recipe(cls, recipe_id):
        recipe_tuple = cls.db.get_recipe(recipe_id)

        if recipe_tuple is not None:
            return Recipe(*recipe_tuple)
        else:
            return None

    @classmethod
    def get_all_recipes(cls):
        recipe_tuples = cls.db.get_all_recipes()
        return [Recipe(*r) for r in recipe_tuples]

    @classmethod
    def get_recipes_by_craft_levels(cls, wood, smith, gold, cloth, leather, bone, alchemy, cook):
        recipe_tuples = cls.db.get_recipes_by_craft_levels(wood, smith, gold, cloth, leather, bone, alchemy, cook)
        return [Recipe(*r) for r in recipe_tuples]

    @classmethod
    def search_recipe(cls, search_term):
        recipe_tuples = cls.db.search_recipe(search_term)
        return [Recipe(*r) for r in recipe_tuples]
