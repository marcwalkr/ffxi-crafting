from database import Database
from helpers import add_nones, remove_nones, sort_alphabetically


class Recipe:
    db = Database()

    def __init__(self, name, crystal, ingredients, synth_yield) -> None:
        self.name = name
        self.crystal = crystal

        # Add empty strings to represent empty ingredient slots for database
        empty_slots = 8 - len(ingredients)
        self.ingredients = add_nones(ingredients, empty_slots)

        self.synth_yield = synth_yield
        self.synth_cost = self.calculate_synth_cost()

    def add_to_database(self):
        self.db.add_recipe(self)

    def calculate_synth_cost(self):
        cost = 0

        for ingredient in [self.crystal] + remove_nones(self.ingredients):
            prices = []

            # Get auction listings (single and stack), append price for single
            # item, price / quantity if it's a stack listing
            listings = self.db.get_auction_listings(ingredient)
            for listing in listings:
                quantity, price = listing[1:3]
                single_price = price / quantity
                prices.append(single_price)

            # Get the item for the vendor price
            item = self.db.get_item(ingredient)

            if item is None:
                raise ValueError("Failed to calculate recipe cost: an " +
                                 "ingredient was not found in the items table")

            vendor_price = item[5]
            if vendor_price is not None:
                prices.append(vendor_price)

            # Get all recipes for this ingredient and append the single cost
            recipes = self.get_recipes(ingredient)
            for recipe in recipes:
                single_cost = recipe.synth_cost / recipe.synth_yield
                prices.append(single_cost)

            cheapest = min(prices)
            cost += cheapest

        return cost

    @classmethod
    def get_recipes(cls, recipe_name):
        recipes = []
        recipe_tuples = cls.db.get_recipes(recipe_name)
        for recipe_tuple in recipe_tuples:
            recipe = cls.from_tuple(recipe_tuple)
            recipes.append(recipe)

        return recipes

    @classmethod
    def get_all_recipes(cls):
        all_recipes = []
        all_recipe_tuples = cls.db.get_all_recipes()
        for recipe_tuple in all_recipe_tuples:
            recipe = cls.from_tuple(recipe_tuple)
            all_recipes.append(recipe)

        sorted = sort_alphabetically(all_recipes)

        return sorted

    @classmethod
    def remove_recipe(cls, name, crystal, ingredients):
        cls.db.remove_recipe(name, crystal, ingredients)

    @classmethod
    def update_recipe_costs(cls):
        # Synth cost gets calculated in constructor
        # Update the database with the new costs
        recipes = cls.get_all_recipes()
        for recipe in recipes:
            cls.db.update_recipe_synth_cost(recipe.name, recipe.synth_cost)

    @classmethod
    def is_in_database(cls, name, crystal, ingredients):
        return cls.db.recipe_is_in_database(name, crystal, ingredients)

    @classmethod
    def from_tuple(cls, recipe_tuple):
        name, crystal = recipe_tuple[0:2]
        ingredients = list(recipe_tuple[2:10])
        synth_yield = recipe_tuple[10]
        recipe = cls(name, crystal, ingredients, synth_yield)
        return recipe
