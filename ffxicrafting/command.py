from prettytable import PrettyTable
from config import Config
from crafted_product import CraftedProduct
from crafter import Crafter
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from controllers.auction_controller import AuctionController
from auction_monitor import AuctionMonitor


class Command:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_command():
        command = input("1. Print crafted products\n" +
                        "2. Print recipe\n" +
                        "3. Monitor auctions\n" +
                        "4. Update auction data\n" +
                        "Q. Quit\n")
        return command

    @classmethod
    def print_crafted_products(cls):
        kiimomo_skill_set = Config.get_skill_set("Kiimomo")
        kiimomo_key_items = Config.get_key_items("Kiimomo")

        alaula_skill_set = Config.get_skill_set("Alaula")
        alaula_key_items = Config.get_key_items("Alaula")

        stronks_skill_set = Config.get_skill_set("Stronks")
        stronks_key_items = Config.get_key_items("Stronks")

        kiimomo = Crafter(kiimomo_skill_set, kiimomo_key_items)
        alaula = Crafter(alaula_skill_set, alaula_key_items)
        stronks = Crafter(stronks_skill_set, stronks_key_items)

        crafters = [kiimomo, alaula, stronks]

        profit, frequency, value = Config.get_thresholds()
        sort_column = Config.get_sort_column()

        products = CraftedProduct.get_products(crafters, profit, frequency,
                                               value, sort_column)

        rows = []
        for product in products:
            recipe_id = product.recipe_id
            item_name = product.item_name
            quantity = product.quantity
            cost = round(product.cost, 2)
            sell_price = round(product.sell_price, 2)
            profit = round(product.profit, 2)
            sell_frequency = round(product.sell_frequency, 2)
            value = round(product.value, 2)

            row = [recipe_id, item_name, quantity, cost, sell_price, profit,
                   sell_frequency, value]
            rows.append(row)

        table = cls.get_table(["Recipe ID", "Item", "Quantity", "Cost",
                               "Average Price", "Profit", "Average Frequency",
                               "Value Score"], rows)
        print(table)

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

        skill_table = cls.get_table(["Wood", "Smith", "Gold", "Cloth",
                                     "Leather", "Bone", "Alchemy", "Cook"],
                                    [[wood, smith, gold, cloth, leather, bone,
                                     alchemy, cook]])

        recipe_table = cls.get_table(["Result", "Crystal", "Ingredient 1",
                                      "Ingredient 2", "Ingredient 3", "Ingredient 4",
                                      "Ingredient 5", "Ingredient 6", "Ingredient 7",
                                      "Ingredient 8"], [row])
        print(skill_table)
        print(recipe_table)

    @classmethod
    def monitor_auctions(cls):
        monitored_ids = Config.get_monitored_item_ids()
        auction_monitor = AuctionMonitor(monitored_ids)
        auction_monitor.monitor_auctions()

    @staticmethod
    def get_table(column_names, rows):
        table = PrettyTable(column_names)

        for name in column_names:
            table.align[name] = "l"

        for row in rows:
            table.add_row(row)

        return table

    @classmethod
    def update_auction_data(cls):
        AuctionController.scrape_update_all_auctions()
