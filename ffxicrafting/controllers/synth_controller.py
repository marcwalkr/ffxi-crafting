from database import Database
from models.synth_recipe import SynthRecipe
from controllers.item_controller import ItemController


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
    def get_recipes(cls, skill_set):
        recipes = []
        recipe_tuples = cls.db.get_recipes(skill_set)
        for recipe_tuple in recipe_tuples:
            recipe = SynthRecipe(*recipe_tuple)
            recipes.append(recipe)

        return recipes

    @classmethod
    def get_synth_cost(cls, recipe):
        ingredient_ids = [recipe.crystal, recipe.ingredient1,
                          recipe.ingredient2, recipe.ingredient3,
                          recipe.ingredient4, recipe.ingredient5,
                          recipe.ingredient6, recipe.ingredient7,
                          recipe.ingredient8]

        # Remove zeros (empty ingredient slots)
        ingredient_ids = [i for i in ingredient_ids if i > 0]

        cost = 0
        for id in ingredient_ids:
            item_cost = ItemController.get_item_cost(id)
            cost += item_cost.cost

        return cost
