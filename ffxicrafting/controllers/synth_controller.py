from database import Database
from models.synth_recipe import SynthRecipe


class SynthController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_recipes(cls, skill_set):
        recipes = []
        recipe_tuples = cls.db.get_recipes(skill_set)
        for recipe_tuple in recipe_tuples:
            recipe = SynthRecipe(*recipe_tuple)
            recipes.append(recipe)

        return recipes
