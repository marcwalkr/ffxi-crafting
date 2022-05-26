from auction_scraper import AuctionScraper
from auction_item import AuctionItem
from database import Database


class AuctionController:
    db = Database()

    def __init__(self, item_name) -> None:
        self.item_name = item_name
        self.scraper = None

    def scrape_self(self):
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

    @classmethod
    def get_all_auction_items(cls):
        auction_items = []
        auction_item_tuples = cls.db.get_all_auction_items()
        for auction_item_tuple in auction_item_tuples:
            auction_item = AuctionItem(*auction_item_tuple)
            auction_items.append(auction_item)

        return auction_items

    def add_self(self):
        item_id = self.scraper.item_id
        item_name = self.scraper.item_name

        single_price = self.scraper.single_price
        stack_price = self.scraper.stack_price

        single_frequency = self.scraper.single_frequency
        stack_frequency = self.scraper.stack_frequency

        self.add_auction_item(item_id, item_name, single_price, stack_price,
                              single_frequency, stack_frequency)

    @classmethod
    def add_auction_item(cls, item_id, item_name, single_price, stack_price,
                         single_frequency, stack_frequency):
        auction_item = AuctionItem(item_id, item_name, single_price,
                                   stack_price, single_frequency,
                                   stack_frequency)
        cls.db.add_auction_item(auction_item)

    @classmethod
    def remove_auction_item(cls, item_name):
        cls.db.remove_auction_item(item_name)

    @classmethod
    def exists(cls, item_name):
        auction_item = cls.get_auction_item(item_name)
        return auction_item is not None

    @classmethod
    def update_auction_items(cls):
        auction_items = cls.get_all_auction_items()
        for auction_item in auction_items:
            scraper = AuctionScraper(auction_item.item_name,
                                     auction_item.item_id)
            new_auction_item = AuctionItem(scraper.item_id, scraper.item_name,
                                           scraper.single_price,
                                           scraper.stack_price,
                                           scraper.single_frequency,
                                           scraper.stack_frequency)
            cls.db.update_auction_item(new_auction_item)
