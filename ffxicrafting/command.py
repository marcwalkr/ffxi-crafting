from table import Table
from config import Config
from crafter import Crafter
from synth import Synth
from collections import defaultdict
from synth_table import SynthTable
from auction_spreadsheet import AuctionSpreadsheet
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController


class Command:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_command():
        command = input("1. Print synth table\n" +
                        "2. Print recipe by ID\n" +
                        "3. Simulate synth\n" +
                        "4. Get ingredient amounts\n"
                        "5. Update auction database\n"
                        "Q. Quit\n")
        return command

    @classmethod
    def print_synth_table(cls):
        melonsoda_skill_set = Config.get_skill_set("Melonsoda")
        melonsoda_key_items = Config.get_key_items("Melonsoda")

        rootbeer_skill_set = Config.get_skill_set("Rootbeer")
        rootbeer_key_items = Config.get_key_items("Rootbeer")

        milktea_skill_set = Config.get_skill_set("Milktea")
        milktea_key_items = Config.get_key_items("Milktea")

        melonsoda = Crafter(melonsoda_skill_set, melonsoda_key_items)
        rootbeer = Crafter(rootbeer_skill_set, rootbeer_key_items)
        milktea = Crafter(milktea_skill_set, milktea_key_items)

        crafters = [melonsoda, rootbeer, milktea]

        synth_profit_threshold = Config.get_profit_per_synth()
        storage_profit_threshold = Config.get_profit_per_storage()
        sort_column = Config.get_synth_sort_column()
        reverse_sort = Config.get_reverse_sort()

        table = SynthTable(crafters, synth_profit_threshold,
                           storage_profit_threshold, sort_column,
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

    @classmethod
    def simulate_synth(cls):
        print()
        character = input("Enter character name: ")
        recipe_id = input("Enter recipe ID: ")

        character = character.capitalize()
        recipe_id = int(recipe_id)

        skill_set = Config.get_skill_set(character)
        key_items = Config.get_key_items(character)
        crafter = Crafter(skill_set, key_items)
        recipe = SynthController.get_recipe(recipe_id)
        synth = Synth(recipe, crafter)

        stop = False
        while True:
            num_times = input("Enter the number of synths: ")
            num_times = int(num_times)
            cost = round(synth.calculate_cost() * num_times)
            results, _ = synth.simulate(num_times)

            print()
            print("Cost: {}".format(cost))
            for item_id, amount in results.items():
                item = ItemController.get_item(item_id)

                if item.stack_size > 1:
                    num_stacks = round(amount / item.stack_size, 2)
                    print("{}: {} ({} stacks)".format(item.sort_name, amount,
                                                      num_stacks))
                else:
                    print("{}: {}".format(item.sort_name, amount))
            print()

            do_again = input("Simulate again? (y/n) ")
            if not do_again == "y":
                stop == True
                break

    @classmethod
    def get_ingredient_amounts(cls):
        print()
        character = input("Enter character name: ")
        recipe_id = input("Enter recipe ID: ")

        character = character.capitalize()
        recipe_id = int(recipe_id)

        skill_set = Config.get_skill_set(character)
        key_items = Config.get_key_items(character)
        crafter = Crafter(skill_set, key_items)
        recipe = SynthController.get_recipe(recipe_id)
        synth = Synth(recipe, crafter)

        result_ids = [recipe.result, recipe.result_hq1, recipe.result_hq2,
                      recipe.result_hq3]
        unique_result_ids = list(dict.fromkeys(result_ids))
        items = [ItemController.get_item(i) for i in unique_result_ids]

        goal_amounts = {}

        for item in items:
            item_name = item.sort_name.replace("_", " ").title()
            goal_amount = input("Goal amount for {}: ".format(item_name))
            goal_amounts[item.item_id] = int(goal_amount)

        num_trials = Config.get_simulation_trials()
        total_num_synths = 0

        for _ in range(num_trials):
            goal_complete = False
            num_synths = 0
            current_amounts = defaultdict(lambda: 0)

            while not goal_complete:
                results, _ = synth.simulate(1)
                num_synths += 1
                for item_id, amount in results.items():
                    current_amounts[item_id] += amount

                goal_complete = True
                for item_id, amount in goal_amounts.items():
                    if current_amounts[item_id] < amount:
                        goal_complete = False

            total_num_synths += num_synths

        average_num_synths = round(total_num_synths / num_trials, 2)
        cost = round(synth.calculate_cost() * average_num_synths)
        print("\nAverage number of synths: {}".format(average_num_synths))
        print("Cost: {}\n".format(cost))

        ingredients = [recipe.crystal, recipe.ingredient1, recipe.ingredient2,
                       recipe.ingredient3, recipe.ingredient4,
                       recipe.ingredient5, recipe.ingredient6,
                       recipe.ingredient7, recipe.ingredient8]
        non_empty_ingredients = [i for i in ingredients if i > 0]

        ingredient_amounts = defaultdict(lambda: 0)
        for i in non_empty_ingredients:
            ingredient_amounts[i] += average_num_synths

        for item_id, amount in ingredient_amounts.items():
            item = ItemController.get_item(item_id)
            item_name = item.sort_name.replace("_", " ").title()
            rounded_amount = round(amount) + 1
            print("{}: {}".format(item_name, rounded_amount))

        print()

    @staticmethod
    def update_auction_database():
        auction_spreadsheet = AuctionSpreadsheet()
        auction_spreadsheet.update_auction_database()
        print("Auction database updated\n")
