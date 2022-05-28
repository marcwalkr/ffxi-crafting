from database import Database
from recipe import Recipe
from helpers import add_nones, remove_nones
from auction_controller import AuctionController
from item_controller import ItemController
from vendor_controller import VendorController
from result_controller import ResultController


class RecipeController:
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
    def calculate_synth_cost(cls, recipe):
        cost = 0

        for ingredient in [recipe.crystal] + recipe.ingredients:
            # Look for every method of obtaining the single ingredient
            # (auction, vendor, craft)
            prices = []

            # Get the auction item for the ingredient
            auction_item = AuctionController.get_auction_item(ingredient)

            # Get the item for the stack quantity
            item = ItemController.get_item(ingredient)

            # Append both prices for one
            # single_price and (stack_price / stack_quantity)
            if auction_item.single_price is not None:
                prices.append(auction_item.single_price)

            if auction_item.stack_price is not None:
                single_from_stack = auction_item.stack_price / item.stack_quantity
                prices.append(single_from_stack)

            # Get all vendor items for the ingredient
            vendor_items = VendorController.get_vendor_items(ingredient)
            if len(vendor_items) > 0:
                # Append all of the prices
                for vendor_item in vendor_items:
                    prices.append(vendor_item.price)

            # Find the cost to craft the single ingredient
            synth_results = ResultController.get_results(ingredient)
            for result in synth_results:
                # For now, skip HQ qualities
                # TODO: calculate the cost factoring in HQ and craft skill
                if result.quality_level != "NQ":
                    continue

                result_recipe = cls.get_recipe_by_id(result.recipe_id)
                result_synth_cost = result_recipe.calculate_synth_cost()
                ingredient_cost = result_synth_cost / result.quantity
                prices.append(ingredient_cost)

            # Add the min price (cheapest way to obtain the item) to the cost
            cheapest = min(prices)
            cost += cheapest

        return cost
