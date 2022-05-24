from database import Database
from text_ui import TextUI
from auction_scraper import AuctionScraper
from auction_listing import AuctionListing


class Item:
    db = Database()

    def __init__(self, name, full_name, stack_quantity) -> None:
        self.name = name
        self.full_name = full_name
        self.stack_quantity = stack_quantity

    def to_database(self):
        self.db.add_item(self)

    @classmethod
    def prompt_add_item(cls):
        item_name = TextUI.prompt_item_name()
        stack_quantity = TextUI.prompt_stack_quantity()

        try:
            # Scrape and verify the item exists on AH before everything else
            scraper = AuctionScraper(item_name)

            # Create the item and add to database
            item = cls(item_name, scraper.full_item_name, stack_quantity)
            item.to_database()

            # Create auction listings for single and stack, add to database
            AuctionListing.add_scraped(item_name, scraper)

        except ValueError as e:
            TextUI.print_error(str(e))

    @classmethod
    def prompt_remove_item(cls):
        item_name = TextUI.prompt_item_name()

        if cls.is_in_database(item_name):
            cls.remove_item(item_name)
        else:
            TextUI.print_error_item_not_in_db(item_name)

    @classmethod
    def get_item(cls, name):
        item_tuple = cls.db.get_item(name)
        if item_tuple is not None:
            item = cls(*item_tuple)
            return item
        else:
            return None

    # @classmethod
    # def get_all_items(cls):
    #     all_items = []
    #     all_item_tuples = cls.db.get_all_items()
    #     for item_tuple in all_item_tuples:
    #         item = cls(*item_tuple)
    #         all_items.append(item)

    #     return all_items

    @classmethod
    def remove_item(cls, item_name):
        cls.db.remove_item(item_name)

    @classmethod
    def is_in_database(cls, name):
        return cls.db.item_is_in_database(name)
