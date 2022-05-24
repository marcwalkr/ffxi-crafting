from item import Item
from vendor import Vendor
from vendor_item import VendorItem
from auction_scraper import AuctionScraper
from auction_listing import AuctionListing
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
                        "Q. Quit\n")
        return command

    @classmethod
    def add_item(cls):
        item_name = cls.prompt_item_name()
        stack_quantity = cls.prompt_stack_quantity()

        try:
            # Scrape and verify the item exists on AH before everything else
            scraper = AuctionScraper(item_name)

            # Create the item and add to database
            item = Item(item_name, scraper.full_item_name, stack_quantity)
            item.to_database()

            # Create auction listings for single and stack, add to database
            AuctionListing.add_scraped(item_name, scraper)

        except ValueError as e:
            Logger.print_red(str(e))

    @classmethod
    def add_vendor(cls):
        npc_name, area, coordinates, vendor_type = cls.prompt_vendor()
        vendor = Vendor(npc_name, area, coordinates, vendor_type)
        vendor.to_database()

    @classmethod
    def add_vendor_item(cls):
        item_name = cls.prompt_item_name()
        vendor_name = cls.prompt_vendor_name()
        price = cls.prompt_vendor_price()

        vendor_item = VendorItem(item_name, vendor_name, price)
        vendor_item.to_database()

    @classmethod
    def remove_item(cls):
        item_name = cls.prompt_item_name()

        if Item.is_in_database(item_name):
            Item.remove_item(item_name)
        else:
            Logger.print_red("Item \"{}\" does not exist in the database"
                             .format(item_name))

    @classmethod
    def remove_vendor(cls):
        npc_name = cls.prompt_vendor_name()

        if Vendor.is_in_database(npc_name):
            Vendor.remove_vendor(npc_name)
        else:
            Logger.print_red("Vendor \"{}\" does not exist in the database"
                             .format(npc_name))

    @classmethod
    def remove_vendor_item(cls):
        item_name = cls.prompt_item_name()
        vendor_name = cls.prompt_vendor_name()

        if VendorItem.is_in_database(item_name, vendor_name):
            VendorItem.remove_vendor_item(item_name, vendor_name)
        else:
            Logger.print_red("Item \"{}\" sold by vendor \"{}\""
                             .format(item_name, vendor_name) +
                             " does not exist in the database")

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

    @classmethod
    def prompt_vendor(cls):
        npc_name = cls.prompt_vendor_name()
        area, coordinates = cls.prompt_vendor_area()
        vendor_type = cls.prompt_vendor_type()

        return npc_name, area, coordinates, vendor_type
