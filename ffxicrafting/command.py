from auction_data_controller import AuctionDataController
from auction_listing_controller import AuctionListingController
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
                        "7. Remove auction listings\n" +
                        "Q. Quit\n")
        return command

    @classmethod
    def add_item(cls):
        item_name = cls.prompt_item_name()

        # Check if the item already exists
        item = ItemController.get_item(item_name)

        if item is not None:
            Logger.print_red("The item \"{}\" is already in the database"
                             .format(item_name))
            return

        stack_quantity = cls.prompt_stack_quantity()

        # Scrape and verify the item exists on AH
        auction_data = AuctionDataController.get_auction_data(item_name)

        if auction_data is None:
            Logger.print_red("The item \"{}\" was not found on the AH"
                             .format(item_name))
            return

        # Add the item to the database
        ItemController.add_item(item_name, stack_quantity)

        # Add the auction listings to the database (single and stack)
        AuctionListingController.add_auction_listings(auction_data)

    @classmethod
    def add_vendor(cls):
        npc_name = cls.prompt_vendor_name()

        # Check if the vendor already exists
        vendor = VendorController.get_vendor(npc_name)
        if vendor is not None:
            Logger.print_red("The vendor \"{}\" is already in the database"
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
        vendor_item = VendorItemController.get_vendor_item(item_name,
                                                           vendor_name)
        if vendor_item is not None:
            Logger.print_red("The item \"{}\"".format(item_name) +
                             " sold by vendor \"{}\"".format(vendor_name) +
                             " is already in the database")
            return

        price = cls.prompt_vendor_price()

        # Add the vendor item to the database
        VendorItemController.add_vendor_item(item_name, vendor_name, price)

    @classmethod
    def remove_item(cls):
        item_name = cls.prompt_item_name()

        # Verify that the item exists
        item = ItemController.get_item(item_name)
        if item is not None:
            ItemController.remove_item(item_name)
        else:
            Logger.print_red("Item \"{}\" does not exist in the database"
                             .format(item_name))

    @classmethod
    def remove_vendor(cls):
        npc_name = cls.prompt_vendor_name()

        # Verify that the vendor exists
        vendor = VendorController.get_vendor(npc_name)
        if vendor is not None:
            VendorController.remove_vendor(npc_name)
        else:
            Logger.print_red("Vendor \"{}\" does not exist in the database"
                             .format(npc_name))

    @classmethod
    def remove_vendor_item(cls):
        item_name = cls.prompt_item_name()
        vendor_name = cls.prompt_vendor_name()

        # Verify that the vendor item exists
        vendor_item = VendorItemController.get_vendor_item(
            item_name, vendor_name)
        if vendor_item is not None:
            VendorItemController.remove_vendor_item(item_name, vendor_name)
        else:
            Logger.print_red("Item \"{}\" sold by vendor \"{}\""
                             .format(item_name, vendor_name) +
                             " does not exist in the database")

    @classmethod
    def remove_auction_listings(cls):
        item_name = cls.prompt_item_name()

        # Verify that a listing exists
        if AuctionListingController.is_in_database(item_name):
            AuctionListingController.remove_auction_listings(item_name)
        else:
            Logger.print_red("Auction listings for item " +
                             "\"{}\" do not exist in the database"
                             .format(item_name))

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
