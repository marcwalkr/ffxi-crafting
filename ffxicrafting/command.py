from auction_item_controller import AuctionItemController
from vendor_item_controller import VendorItemController
from vendor_controller import VendorController
from item_controller import ItemController
from logger import Logger


class Command:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_command():
        command = input("1. Add an item\n" +
                        "2. Add a vendor\n" +
                        "3. Add a vendor item\n" +
                        "4. Remove an item\n" +
                        "5. Remove a vendor\n" +
                        "6. Remove a vendor item\n" +
                        "7. Remove an auction item\n" +
                        "8. Update auction prices and frequencies\n" +
                        "Q. Quit\n")
        return command

    @classmethod
    def add_item(cls):
        item_name = cls.prompt_item_name()

        # Check if the item already exists
        if ItemController.is_in_database(item_name):
            Logger.print_red("Item \"{}\" is already in the database"
                             .format(item_name))
            return

        stack_quantity = cls.prompt_stack_quantity()

        # Scrape and verify the item exists on AH
        auction_item_controller = AuctionItemController(item_name)
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
        if VendorController.is_in_database(npc_name):
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
        if VendorItemController.is_in_database(item_name, vendor_name):
            Logger.print_red("Vendor item \"{}\"".format(item_name) +
                             " sold by \"{}\"".format(vendor_name) +
                             " is already in the database")
            return

        price = cls.prompt_vendor_price()

        # Add the vendor item to the database
        VendorItemController.add_vendor_item(item_name, vendor_name, price)

    @classmethod
    def remove_item(cls):
        item_name = cls.prompt_item_name()

        # Verify that the item exists
        if ItemController.is_in_database(item_name):
            ItemController.remove_item(item_name)
        else:
            Logger.print_red("Item \"{}\" does not exist in the database"
                             .format(item_name))

    @classmethod
    def remove_vendor(cls):
        npc_name = cls.prompt_vendor_name()

        # Verify that the vendor exists
        if VendorController.is_in_database(npc_name):
            VendorController.remove_vendor(npc_name)
        else:
            Logger.print_red("Vendor \"{}\" does not exist in the database"
                             .format(npc_name))

    @classmethod
    def remove_vendor_item(cls):
        item_name = cls.prompt_item_name()
        vendor_name = cls.prompt_vendor_name()

        # Verify that the vendor item exists
        if VendorItemController.is_in_database(item_name, vendor_name):
            VendorItemController.remove_vendor_item(item_name, vendor_name)
        else:
            Logger.print_red("Item \"{}\" sold by vendor \"{}\""
                             .format(item_name, vendor_name) +
                             " does not exist in the database")

    @classmethod
    def remove_auction_item(cls):
        item_name = cls.prompt_item_name()

        # Verify that a listing exists
        if AuctionItemController.is_in_database(item_name):
            AuctionItemController.remove_auction_item(item_name)
        else:
            Logger.print_red("Auction item \"{}\"".format(item_name) +
                             " does not exist in the database")

    @classmethod
    def update_auction_items(cls):
        AuctionItemController.update_auction_items()

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
