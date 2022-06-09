from prettytable import PrettyTable
from config import Config
from product import Product
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from auction_scraper import AuctionScraper
from auction_monitor import AuctionMonitor


class Command:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_command():
        command = input("1. Print products\n" +
                        "2. Print recipe\n" +
                        "3. Print an auction price history\n" +
                        "4. Monitor auctions\n" +
                        "Q. Quit\n")
        return command

    @classmethod
    def print_products(cls):
        skill_set = Config.get_skill_set()
        profit_threshold, freq_threshold = Config.get_thresholds()

        products = Product.get_products(skill_set, profit_threshold,
                                        freq_threshold)

        rows = []
        for product in products:
            recipe_id = product.recipe_id
            item_name = product.item_name
            quantity = product.quantity
            cost = round(product.cost, 2)
            sell_price = product.sell_price
            profit = round(product.profit, 2)
            sell_frequency = round(product.sell_frequency, 2)
            value = round(product.value, 2)

            row = [recipe_id, item_name, quantity, cost, sell_price, profit,
                   sell_frequency, value]
            rows.append(row)

        table = cls.get_table(["Recipe ID", "Item", "Quantity", "Cost",
                               "Sell Price", "Profit", "Sell Frequency",
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
    def print_auction_history(cls):
        item_id = input("Enter the item id: ")
        scraper = AuctionScraper(item_id)

        rows = []
        for i in range(len(scraper.sellers)):
            seller = scraper.sellers[i]
            buyer = scraper.buyers[i]
            quantity = scraper.quantities[i]
            price = scraper.prices[i]
            date = scraper.dates[i]

            rows.append([seller, buyer, quantity, price, date])

        table = cls.get_table(["Seller", "Buyer", "Quantity", "Price", "Date"],
                              rows)
        print(table)

    @classmethod
    def monitor_auctions(cls):
        monitored_ids = Config.get_monitored_item_ids()
        frequency = Config.get_monitor_frequency()
        auction_monitor = AuctionMonitor(monitored_ids, frequency)
        auction_monitor.monitor_auctions()

    @staticmethod
    def get_table(column_names, rows):
        table = PrettyTable(column_names)

        for name in column_names:
            table.align[name] = "l"

        for row in rows:
            table.add_row(row)

        return table
