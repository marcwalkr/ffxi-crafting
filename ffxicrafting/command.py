from table import Table
from config import Config
from models.crafter import Crafter
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from controllers.auction_controller import AuctionController
from auction_monitor import AuctionMonitor
from product_table import ProductTable


class Command:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_command():
        command = input("1. Print product table\n" +
                        "2. Print recipe\n" +
                        "3. Monitor auctions\n" +
                        "4. Update auction data\n" +
                        "Q. Quit\n")
        return command

    @classmethod
    def print_product_table(cls):
        char1_skill_set = Config.get_skill_set("Character1")
        char1_key_items = Config.get_key_items("Character1")

        char2_skill_set = Config.get_skill_set("Character2")
        char2_key_items = Config.get_key_items("Character2")

        char3_skill_set = Config.get_skill_set("Character3")
        char3_key_items = Config.get_key_items("Character3")

        character1 = Crafter(char1_skill_set, char1_key_items)
        character2 = Crafter(char2_skill_set, char2_key_items)
        character3 = Crafter(char3_skill_set, char3_key_items)

        recipes = SynthController.get_all_recipes()
        crafters = [character1, character2, character3]

        include_desynth = Config.get_include_desynth()
        skill_look_ahead = Config.get_skill_look_ahead()
        profit_threshold = Config.get_profit_threshold()
        frequency_threshold = Config.get_frequency_threshold()
        sort_column = Config.get_sort_column()

        table = ProductTable(recipes, crafters, include_desynth,
                             skill_look_ahead, profit_threshold,
                             frequency_threshold, sort_column)
        table.print()

    @classmethod
    def print_recipe(cls):
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

    @classmethod
    def monitor_auctions(cls):
        monitored_ids = Config.get_monitored_item_ids()
        auction_monitor = AuctionMonitor(monitored_ids)
        auction_monitor.monitor_auctions()

    @classmethod
    def update_auction_data(cls):
        AuctionController.update_auction_data()
