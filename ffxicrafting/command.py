from product import Product
from models.skill_set import SkillSet
from logger import Logger
from prettytable import PrettyTable


class Command:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_command():
        command = input("1. Print products\n" +
                        "Q. Quit\n")
        return command

    @classmethod
    def update_auction_items(cls):
        pass

    @classmethod
    def print_products(cls):
        skill_set = cls.prompt_skill_set()
        profit_threshold, freq_threshold = cls.prompt_thresholds()

        products = Product.get_products(skill_set, profit_threshold,
                                        freq_threshold)

        # # Sort by value (profit * sell frequency)
        # sorted_products = sorted(products, key=lambda x: x.value, reverse=True)

        # rows = []
        # for product in sorted_products:
        #     row = [product.item_name, product.quantity, round(product.cost, 2),
        #            product.sell_price, round(product.profit, 2),
        #            round(product.sell_frequency, 2), round(product.value, 2)]
        #     rows.append(row)

        # table = cls.get_table(["Item", "Quantity", "Cost", "Sell Price",
        #                        "Profit", "Sell Frequency", "Value Score"], rows)
        # print(table)

    @staticmethod
    def prompt_thresholds():
        profit_threshold = input("Enter the profit threshold: ")
        freq_threshold = input("Enter the frequency threshold: ")

        profit_threshold = int(profit_threshold)
        freq_threshold = int(freq_threshold)

        return profit_threshold, freq_threshold

    @staticmethod
    def prompt_skill_set():
        wood = input("Enter woodworking skill: ")
        smith = input("Enter smithing skill: ")
        gold = input("Enter goldsmithing skill: ")
        cloth = input("Enter clothcraft skill: ")
        leather = input("Enter leathercraft skill: ")
        bone = input("Enter bonecraft skill: ")
        alchemy = input("Enter alchemy skill: ")
        cook = input("Enter cooking skill: ")

        wood = int(wood)
        smith = int(smith)
        gold = int(gold)
        cloth = int(cloth)
        leather = int(leather)
        bone = int(bone)
        alchemy = int(alchemy)
        cook = int(cook)

        return SkillSet(wood, smith, gold, cloth, leather, bone, alchemy, cook)

    @staticmethod
    def get_table(column_names, rows):
        table = PrettyTable(column_names)

        for name in column_names:
            table.align[name] = "l"

        for row in rows:
            table.add_row(row)

        return table
