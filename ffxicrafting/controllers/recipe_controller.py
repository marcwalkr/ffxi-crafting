import logging
from entities import Recipe
from repositories import RecipeRepository
from controllers import ItemController

logger = logging.getLogger(__name__)


class RecipeController:
    recipe_cache = {}

    def __init__(self, db) -> None:
        self.item_controller = ItemController(db)
        self.recipe_repository = RecipeRepository(db)

    def get_recipe(self, recipe_id):
        if recipe_id in self.recipe_cache:
            return self.recipe_cache[recipe_id]
        else:
            raise ValueError(f"Recipe with id {recipe_id} not found in cache.")

    def get_recipes_by_level(self, *craft_levels, batch_size, offset):
        recipe_models = self.recipe_repository.get_recipes_by_level(*craft_levels, batch_size=batch_size, offset=offset)
        if recipe_models:
            recipes = self.process_and_cache_recipes(recipe_models)
            self.recipe_cache.update({recipe.id: recipe for recipe in recipes})
            return recipes
        else:
            return []

    def search_recipe(self, search_term, batch_size, offset):
        recipe_models = self.recipe_repository.search_recipe(search_term, batch_size, offset)
        if recipe_models:
            recipes = self.process_and_cache_recipes(recipe_models)
            self.recipe_cache.update({recipe.id: recipe for recipe in recipes})
            return recipes
        else:
            return []

    def process_and_cache_recipes(self, recipe_models):
        ingredient_item_ids = set()
        result_item_ids = set()

        for recipe_model in recipe_models:
            # Treat the crystal as an ingredient
            ingredient_item_ids.add(recipe_model.crystal)

            # Gather ingredient ids
            ingredient_item_ids.update([recipe_model.ingredient1, recipe_model.ingredient2, recipe_model.ingredient3,
                                       recipe_model.ingredient4, recipe_model.ingredient5, recipe_model.ingredient6,
                                       recipe_model.ingredient7, recipe_model.ingredient8])

            # Remove empty ingredients represented by 0
            ingredient_item_ids.discard(0)

            # Gather result ids
            result_item_ids.update([recipe_model.result, recipe_model.result_hq1, recipe_model.result_hq2,
                                   recipe_model.result_hq3])

        ingredients, results = self.item_controller.get_recipe_items(list(ingredient_item_ids), list(result_item_ids))

        recipes = []
        for recipe_model in recipe_models:
            if recipe_model.id in self.recipe_cache:
                recipes.append(self.recipe_cache[recipe_model.id])
            else:
                recipe = self.create_recipe_object(recipe_model, ingredients, results)
                self.recipe_cache[recipe_model.id] = recipe
                recipes.append(recipe)
        return recipes

    def create_recipe_object(self, recipe_model, ingredients, results):
        recipe = Recipe(
            recipe_model.id, recipe_model.desynth, recipe_model.key_item, recipe_model.wood, recipe_model.smith,
            recipe_model.gold, recipe_model.cloth, recipe_model.leather, recipe_model.bone, recipe_model.alchemy,
            recipe_model.cook, recipe_model.crystal, recipe_model.hq_crystal, recipe_model.ingredient1,
            recipe_model.ingredient2, recipe_model.ingredient3, recipe_model.ingredient4, recipe_model.ingredient5,
            recipe_model.ingredient6, recipe_model.ingredient7, recipe_model.ingredient8, recipe_model.result,
            recipe_model.result_hq1, recipe_model.result_hq2, recipe_model.result_hq3, recipe_model.result_qty,
            recipe_model.result_hq1_qty, recipe_model.result_hq2_qty, recipe_model.result_hq3_qty,
            recipe_model.result_name,
            next((ingredient for ingredient in ingredients if ingredient.item_id == recipe_model.crystal), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == recipe_model.ingredient1), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == recipe_model.ingredient2), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == recipe_model.ingredient3), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == recipe_model.ingredient4), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == recipe_model.ingredient5), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == recipe_model.ingredient6), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == recipe_model.ingredient7), None),
            next((ingredient for ingredient in ingredients if ingredient.item_id == recipe_model.ingredient8), None),
            next((result for result in results if result.item_id == recipe_model.result), None),
            next((result for result in results if result.item_id == recipe_model.result_hq1), None),
            next((result for result in results if result.item_id == recipe_model.result_hq2), None),
            next((result for result in results if result.item_id == recipe_model.result_hq3), None)
        )
        return recipe
