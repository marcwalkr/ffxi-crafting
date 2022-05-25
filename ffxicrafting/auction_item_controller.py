from auction_scraper import AuctionScraper
from auction_item import AuctionItem
from database import Database


class AuctionItemController:
    db = Database()

    def __init__(self, item_name) -> None:
        self.item_name = item_name
        self.scraper = None

    def scrape_auction_item(self):
        self.scraper = AuctionScraper(self.item_name)
        if self.scraper.item_id is not None:
            return True

        return False

    @classmethod
    def get_auction_item(cls, item_name):
        auction_item_tuple = cls.db.get_auction_item(item_name)
        if auction_item_tuple is not None:
            return AuctionItem(*auction_item_tuple)

        return None

    def add_auction_item(self):
        item_id = self.scraper.item_id
        item_name = self.scraper.item_name

        single_price = self.scraper.single_price
        stack_price = self.scraper.stack_price

        single_frequency = self.scraper.single_frequency
        stack_frequency = self.scraper.stack_frequency

        auction_item = AuctionItem(item_id, item_name, single_price,
                                   stack_price, single_frequency,
                                   stack_frequency)

        self.db.add_auction_item(auction_item)

    @classmethod
    def remove_auction_item(cls, item_name):
        cls.db.remove_auction_item(item_name)

    @classmethod
    def is_in_database(cls, item_name):
        auction_item = cls.get_auction_item(item_name)
        return auction_item is not None
