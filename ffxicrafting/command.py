from auction_controller import AuctionController
from vendor_controller import VendorController
from item_controller import ItemController
from synth_controller import SynthController
from product import Product
from logger import Logger
from helpers import expand_list
from prettytable import PrettyTable


class Command:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_command():
        command = input("1. Add an item\n" +
                        "2. Add a vendor\n" +
                        "3. Add a vendor item\n" +
                        "4. Add a recipe\n" +
                        "5. Remove an item\n" +
                        "6. Remove a vendor\n" +
                        "7. Remove a vendor item\n" +
                        "8. Remove an auction item\n" +
                        "9. Remove a recipe\n" +
                        "10. Update a vendor price\n" +
                        "11. Update auction prices and frequencies\n" +
                        "12. Print products\n" +
                        "Q. Quit\n")
        return command

    @classmethod
    def add_item(cls):
        item_name = cls.prompt_item_name()

        # Check if the item already exists
        if ItemController.exists(item_name):
            Logger.print_red("Item \"{}\" is already in the database"
                             .format(item_name))
            return

        stack_quantity = cls.prompt_stack_quantity()

        # Scrape and verify the item exists on AH
        auction_item_controller = AuctionController(item_name)
        item_found = auction_item_controller.scrape_self()

        if not item_found:
            Logger.print_red("Item \"{}\" was not found on the AH"
                             .format(item_name))
            return

        # Add the item to the database
        ItemController.add_item(item_name, stack_quantity)

        # Add the auction item to the database
        auction_item_controller.add_self()

    @classmethod
    def add_vendor(cls):
        npc_name = cls.prompt_vendor_name()

        # Check if the vendor already exists
        if VendorController.vendor_exists(npc_name):
            Logger.print_red("Vendor \"{}\" is already in the database"
                             .format(npc_name))
            return

        area, coordinates = cls.prompt_vendor_area()
        vendor_type = cls.prompt_vendor_type()

        # Add the vendor to the database
        VendorController.add_vendor(npc_name, area, coordinates, vendor_type)

    @classmethod
    def add_vendor_item(cls):
        item_name = cls.prompt_item_name()
        vendor_name = cls.prompt_vendor_name()

        # Check if the vendor item already exists
        if VendorController.vendor_item_exists(item_name, vendor_name):
            Logger.print_red("Vendor item \"{}\"".format(item_name) +
                             " sold by \"{}\"".format(vendor_name) +
                             " is already in the database")
            return

        price = cls.prompt_vendor_price()

        # Add the vendor item to the database
        VendorController.add_vendor_item(item_name, vendor_name, price)

    @classmethod
    def add_recipe(cls):
        crystal = cls.prompt_crystal()
        ingredients = cls.prompt_ingredients()
        alchemy, bonecraft, clothcraft, cooking, goldsmithing, leathercraft, \
            smithing, woodworking = cls.prompt_craft_skills()

        # Check if the recipe already exists
        if SynthController.recipe_exists(crystal, ingredients):
            Logger.print_red("Recipe is already in the database")
            return

        SynthController.add_recipe(crystal, ingredients, alchemy, bonecraft,
                                   clothcraft, cooking, goldsmithing,
                                   leathercraft, smithing, woodworking)

        # Get the id that was generated when the recipe was added
        recipe_id = SynthController.get_recipe_id(crystal, ingredients)

        # Get the items and quantities of all of the quality levels
        nq_item, hq1_item, hq2_item, hq3_item, nq_quantity, hq1_quantity, \
            hq2_quantity, hq3_quantity = cls.prompt_quality_levels()

        # Add synthesis results
        SynthController.add_result(nq_item, recipe_id, nq_quantity, "NQ")
        SynthController.add_result(hq1_item, recipe_id, hq1_quantity, "HQ1")
        SynthController.add_result(hq2_item, recipe_id, hq2_quantity, "HQ2")
        SynthController.add_result(hq3_item, recipe_id, hq3_quantity, "HQ3")

    @classmethod
    def remove_item(cls):
        item_name = cls.prompt_item_name()

        # Verify that the item exists
        if ItemController.exists(item_name):
            ItemController.remove_item(item_name)
        else:
            Logger.print_red("Item \"{}\" does not exist in the database"
                             .format(item_name))

    @classmethod
    def remove_vendor(cls):
        npc_name = cls.prompt_vendor_name()

        # Verify that the vendor exists
        if VendorController.vendor_exists(npc_name):
            VendorController.remove_vendor(npc_name)
        else:
            Logger.print_red("Vendor \"{}\" does not exist in the database"
                             .format(npc_name))

    @classmethod
    def remove_vendor_item(cls):
        item_name = cls.prompt_item_name()
        vendor_name = cls.prompt_vendor_name()

        # Verify that the vendor item exists
        if VendorController.vendor_item_exists(item_name, vendor_name):
            VendorController.remove_vendor_item(item_name, vendor_name)
        else:
            Logger.print_red("Item \"{}\" sold by vendor \"{}\""
                             .format(item_name, vendor_name) +
                             " does not exist in the database")

    @classmethod
    def remove_auction_item(cls):
        item_name = cls.prompt_item_name()

        # Verify that a listing exists
        if AuctionController.exists(item_name):
            AuctionController.remove_auction_item(item_name)
        else:
            Logger.print_red("Auction item \"{}\"".format(item_name) +
                             " does not exist in the database")

    @classmethod
    def remove_recipe(cls):
        crystal = cls.prompt_crystal()
        ingredients = cls.prompt_ingredients()

        # Verify that the recipe exists
        if SynthController.recipe_exists(crystal, ingredients):
            SynthController.remove_recipe(crystal, ingredients)
        else:
            Logger.print_red("Recipe does not exist in the database")

    @classmethod
    def update_vendor_price(cls):
        item_name = cls.prompt_item_name()
        vendor_name = cls.prompt_vendor_name()
        price = cls.prompt_vendor_price()

        VendorController.update_vendor_price(item_name, vendor_name, price)

    @classmethod
    def update_auction_items(cls):
        AuctionController.update_auction_items()

    @classmethod
    def print_products(cls):
        profit_threshold, freq_threshold = cls.prompt_thresholds()

        products = Product.get_products(profit_threshold, freq_threshold)

        rows = []
        for product in products:
            row = [product.item_name, product.quantity, product.cost,
                   product.sell_price, product.profit, product.sell_frequency]
            rows.append(row)

        table = cls.get_table(["Name", "Quantity", "Cost", "Sell Price",
                               "Profit", "Sell Frequency"], rows)
        print(table)

    @staticmethod
    def prompt_item_name():
        return input("Enter the item name: ")

    @staticmethod
    def prompt_stack_quantity():
        stackable = input("Is it stackable? (y/n): ")
        if stackable == "y":
            stack_quantity = input("Enter the stack quantity: ")
            stack_quantity = int(stack_quantity)
        else:
            stack_quantity = None

        return stack_quantity

    @staticmethod
    def prompt_vendor_name():
        return input("Enter the vendor name: ")

    @staticmethod
    def prompt_vendor_area():
        area = input("Enter the area name abbreviation: ")
        coordinates = input("Enter the coordinates: ")

        return area, coordinates

    @staticmethod
    def prompt_vendor_type():
        return input("Enter the vendor type (Standard, Guild, Regional): ")

    @staticmethod
    def prompt_vendor_price():
        price = input("Enter the price: ")
        return int(price)

    @staticmethod
    def prompt_crystal():
        return input("Enter the crystal: ")

    @staticmethod
    def prompt_ingredients():
        ingredients = input(("Enter the list of ingredients separated by "
                             "commas: "))
        ingredients = ingredients.split(", ")
        ingredients = expand_list(ingredients)

        return ingredients

    @staticmethod
    def prompt_craft_skills():
        alchemy = input("Enter the alchemy skill: ")
        bonecraft = input("Enter the bonecraft skill: ")
        clothcraft = input("Enter the clothcraft skill: ")
        cooking = input("Enter the cooking skill: ")
        goldsmithing = input("Enter the goldsmithing skill: ")
        leathercraft = input("Enter the leathercraft skill: ")
        smithing = input("Enter the smithing skill: ")
        woodworking = input("Enter the woodworking skill: ")

        return alchemy, bonecraft, clothcraft, cooking, goldsmithing, \
            leathercraft, smithing, woodworking

    @staticmethod
    def prompt_quality_levels():
        nq_item = input("Enter the NQ item: ")

        different_items = input("Does HQ produce different items? (y/n): ")

        if different_items == "y":
            hq1_item = input("Enter the HQ1 item: ")
            hq2_item = input("Enter the HQ2 item: ")
            hq3_item = input("Enter the HQ3 item: ")
        else:
            hq1_item = nq_item
            hq2_item = nq_item
            hq3_item = nq_item

        nq_quantity = input("Enter the NQ quantity: ")
        hq1_quantity = input("Enter the HQ1 quantity: ")
        hq2_quantity = input("Enter the HQ2 quantity: ")
        hq3_quantity = input("Enter the HQ3 quantity: ")

        nq_quantity = int(nq_quantity)
        hq1_quantity = int(hq1_quantity)
        hq2_quantity = int(hq2_quantity)
        hq3_quantity = int(hq3_quantity)

        return nq_item, hq1_item, hq2_item, hq3_item, nq_quantity, \
            hq1_quantity, hq2_quantity, hq3_quantity

    @staticmethod
    def prompt_thresholds():
        profit_threshold = input("Enter the profit threshold: ")
        freq_threshold = input("Enter the frequency threshold: ")

        profit_threshold = int(profit_threshold)
        freq_threshold = int(freq_threshold)

        return profit_threshold, freq_threshold

    @staticmethod
    def get_table(column_names, rows):
        table = PrettyTable(column_names)

        for name in column_names:
            table.align[name] = "l"

        for row in rows:
            table.add_row(row)

        return table
