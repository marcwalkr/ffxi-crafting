from table import Table
from config import Config
from crafter import Crafter
from synth_table import SynthTable
from product_table import ProductTable
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController


class Command:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_command():
        command = input("1. Print synth table\n" +
                        "2. Print product table\n" +
                        "3. Print recipe by ID\n" +
                        "Q. Quit\n")
        return command

    @staticmethod
    def print_synth_table():
        skill_set = Config.get_skill_set()
        key_items = Config.get_key_items()

        crafter = Crafter(skill_set, key_items)

        synth_profit_threshold = Config.get_profit_per_synth()
        inventory_profit_threshold = Config.get_profit_per_inventory()
        sort_column = Config.get_synth_sort_column()
        reverse_sort = Config.get_reverse_sort()

        table = SynthTable(crafter, synth_profit_threshold,
                           inventory_profit_threshold, sort_column,
                           reverse_sort)
        table.print()

    @staticmethod
    def print_product_table():
        skill_set = Config.get_skill_set()
        key_items = Config.get_key_items()

        crafter = Crafter(skill_set, key_items)

        profit_threshold = Config.get_profit_per_product()
        sort_column = Config.get_product_sort_column()
        reverse_sort = Config.get_reverse_sort()

        table = ProductTable(crafter, profit_threshold, sort_column,
                             reverse_sort)
        table.print()

    @staticmethod
    def print_recipe():
        recipe_id = input("Enter the recipe id: ")
        recipe = SynthController.get_recipe(recipe_id)

        item_ids = [recipe.crystal, recipe.ingredient1, recipe.ingredient2,
                    recipe.ingredient3, recipe.ingredient4, recipe.ingredient5,
                    recipe.ingredient6, recipe.ingredient7, recipe.ingredient8]

        row = [recipe.result_name]

        for id in item_ids:
            if id == 0:
                row.append("")
            else:
                item = ItemController.get_item(id)
                name = item.sort_name.replace("_", " ").title()
                row.append(name)

        wood = str(recipe.wood)
        smith = str(recipe.smith)
        gold = str(recipe.gold)
        cloth = str(recipe.cloth)
        leather = str(recipe.leather)
        bone = str(recipe.bone)
        alchemy = str(recipe.alchemy)
        cook = str(recipe.cook)

        skill_table = Table(["Wood", "Smith", "Gold", "Cloth", "Leather",
                             "Bone", "Alchemy", "Cook"],
                            [[wood, smith, gold, cloth, leather, bone,
                              alchemy, cook]])

        recipe_table = Table(["Result", "Crystal", "Ingredient 1",
                              "Ingredient 2", "Ingredient 3", "Ingredient 4",
                              "Ingredient 5", "Ingredient 6", "Ingredient 7",
                              "Ingredient 8"], [row])

        skill_table.print()
        recipe_table.print()
