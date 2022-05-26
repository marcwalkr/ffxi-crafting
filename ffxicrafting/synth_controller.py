from database import Database
from recipe import Recipe
from synthesis_result import SynthesisResult


class SynthController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_recipe_id(cls, crystal, ingredients):
        result = cls.db.get_recipe(crystal, ingredients)
        if result is not None:
            return result[0]

        return None

    @classmethod
    def add_recipe(cls, crystal, ingredients, craft, skill_cap):
        recipe = Recipe(crystal, ingredients, craft, skill_cap)
        cls.db.add_recipe(recipe)

    @classmethod
    def remove_recipe(cls, crystal, ingredients):
        cls.db.remove_recipe(crystal, ingredients)

    @classmethod
    def add_result(cls, item_name, recipe_id, quantity, quality_level):
        result = SynthesisResult(item_name, recipe_id, quantity, quality_level)
        cls.db.add_synthesis_result(result)

    @classmethod
    def recipe_exists(cls, crystal, ingredients):
        return cls.db.get_recipe(crystal, ingredients) is not None
