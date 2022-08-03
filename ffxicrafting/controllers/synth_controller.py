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
    def get_recipes(cls, skill_set, skill_range):
        recipes = []
        recipe_tuples = cls.db.get_recipes(skill_set, skill_range)
        for recipe_tuple in recipe_tuples:
            recipe = SynthRecipe(*recipe_tuple)
            recipes.append(recipe)

        return recipes

    @classmethod
    def get_all_recipes(cls):
        recipes = []
        recipe_tuples = cls.db.get_all_recipes()
        for recipe_tuple in recipe_tuples:
            recipe = SynthRecipe(*recipe_tuple)
            recipes.append(recipe)

        return recipes
