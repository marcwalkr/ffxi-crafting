from database import Database
from models.synth_recipe import SynthRecipe


class SynthController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_recipe(cls, recipe_id):
        recipe_tuple = cls.db.get_recipe(recipe_id)

        if recipe_tuple is not None:
            return SynthRecipe(*recipe_tuple)
        else:
            return None

    @classmethod
    def get_all_recipes(cls):
        recipe_tuples = cls.db.get_all_recipes()
        return [SynthRecipe(*r) for r in recipe_tuples]

    @classmethod
    def search_recipe(cls, search_term):
        recipe_tuples = cls.db.search_recipe(search_term)
        return [SynthRecipe(*r) for r in recipe_tuples]
