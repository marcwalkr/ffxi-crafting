from database import Database
from recipe import Recipe
from synthesis_result import SynthesisResult
from helpers import add_nones, remove_nones


class SynthController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_recipe_id(cls, crystal, ingredients):
        recipe = cls.db.get_recipe(crystal, ingredients)
        if recipe is not None:
            return recipe[0]

        return None

    @classmethod
    def get_recipe_by_id(cls, recipe_id):
        recipe_tuple = cls.db.get_recipe_by_id(recipe_id)
        recipe = cls.tuple_to_recipe(recipe_tuple)
        return recipe

    @classmethod
    def get_all_recipes(cls):
        recipe_tuples = cls.db.get_all_recipes()

        recipes = []
        for recipe_tuple in recipe_tuples:
            recipe = cls.tuple_to_recipe(recipe_tuple)
            recipes.append(recipe)

        return recipes

    @classmethod
    def add_recipe(cls, crystal, ingredients, craft, skill_cap):
        # Add Nones to represent empty ingredient slots
        empty_slots = 8 - len(ingredients)
        full_ingredients = add_nones(ingredients, empty_slots)

        recipe = Recipe(crystal, full_ingredients, craft, skill_cap)
        cls.db.add_recipe(recipe)

    @classmethod
    def remove_recipe(cls, crystal, ingredients):
        cls.db.remove_recipe(crystal, ingredients)

    @classmethod
    def recipe_exists(cls, crystal, ingredients):
        return cls.db.get_recipe(crystal, ingredients) is not None

    @classmethod
    def tuple_to_recipe(cls, recipe_tuple):
        crystal = recipe_tuple[1]
        ingredients = list(recipe_tuple[2:10])
        ingredients = remove_nones(ingredients)
        craft, skill_cap = recipe_tuple[10:]
        return Recipe(crystal, ingredients, craft, skill_cap)

    @classmethod
    def get_results(cls, item_name):
        result_tuples = cls.db.get_synthesis_results(item_name)

        results = []
        for result_tuple in result_tuples:
            result = SynthesisResult(*result_tuple)
            results.append(result)

        return results

    @classmethod
    def get_all_results(cls):
        result_tuples = cls.db.get_all_synthesis_results()

        results = []
        for result_tuple in result_tuples:
            result = SynthesisResult(*result_tuple)
            results.append(result)

        return results

    @classmethod
    def add_result(cls, item_name, recipe_id, quantity, quality_level):
        result = SynthesisResult(item_name, recipe_id, quantity, quality_level)
        cls.db.add_synthesis_result(result)
