from table import Table
from config import Config
from crafter import Crafter
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from controllers.auction_controller import AuctionController
from auction_monitor import AuctionMonitor
from synth_table import SynthTable


class Command:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_command():
        command = input("1. Print synth table\n" +
                        "2. Print recipe\n" +
                        "3. Monitor auctions\n" +
                        "4. Update auction data\n" +
                        "Q. Quit\n")
        return command

    @classmethod
    def print_synth_table(cls):
        char1_skill_set = Config.get_skill_set("Character1")
        char1_key_items = Config.get_key_items("Character1")

        char2_skill_set = Config.get_skill_set("Character2")
        char2_key_items = Config.get_key_items("Character2")

        char3_skill_set = Config.get_skill_set("Character3")
        char3_key_items = Config.get_key_items("Character3")

        character1 = Crafter(char1_skill_set, char1_key_items)
        character2 = Crafter(char2_skill_set, char2_key_items)
        character3 = Crafter(char3_skill_set, char3_key_items)

        crafters = [character1, character2, character3]

        # wood_skill_set = Config.get_skill_set("TestWood")
        # smith_skill_set = Config.get_skill_set("TestSmith")
        # gold_skill_set = Config.get_skill_set("TestGold")
        # cloth_skill_set = Config.get_skill_set("TestCloth")
        # leather_skill_set = Config.get_skill_set("TestLeather")
        # bone_skill_set = Config.get_skill_set("TestBone")
        # alchemy_skill_set = Config.get_skill_set("TestAlchemy")
        # cook_skill_set = Config.get_skill_set("TestCook")

        # wood_key_items = Config.get_key_items("TestWood")
        # smith_key_items = Config.get_key_items("TestSmith")
        # gold_key_items = Config.get_key_items("TestGold")
        # cloth_key_items = Config.get_key_items("TestCloth")
        # leather_key_items = Config.get_key_items("TestLeather")
        # bone_key_items = Config.get_key_items("TestBone")
        # alchemy_key_items = Config.get_key_items("TestAlchemy")
        # cook_key_items = Config.get_key_items("TestCook")

        # wood = Crafter(wood_skill_set, wood_key_items)
        # smith = Crafter(smith_skill_set, smith_key_items)
        # gold = Crafter(gold_skill_set, gold_key_items)
        # cloth = Crafter(cloth_skill_set, cloth_key_items)
        # leather = Crafter(leather_skill_set, leather_key_items)
        # bone = Crafter(bone_skill_set, bone_key_items)
        # alchemy = Crafter(alchemy_skill_set, alchemy_key_items)
        # cook = Crafter(cook_skill_set, cook_key_items)

        # crafters = [wood, smith, gold, cloth, leather, bone, alchemy, cook]

        # test_skill_set = Config.get_skill_set("TestCharacter")
        # test_char = Crafter(test_skill_set)

        # crafters = [test_char]

        recipes = SynthController.get_all_recipes()
        profit_threshold = Config.get_profit_threshold()
        frequency_threshold = Config.get_frequency_threshold()
        sort_column = Config.get_sort_column()
        reverse_sort = Config.get_reverse_sort()

        table = SynthTable(recipes, crafters, profit_threshold,
                           frequency_threshold, sort_column, reverse_sort)
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
