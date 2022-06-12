from database import Database
from helpers import older_than
from models.auction import Auction
from auction_scraper import AuctionScraper


class AuctionController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_auction(cls, item_id):
        auction_tuple = cls.db.get_auction(item_id)

        if auction_tuple is not None:
            auction = Auction(*auction_tuple)

            if older_than(auction.last_updated, 7):
                scraper = AuctionScraper(item_id)
                cls.update_auction(item_id, scraper.single_price,
                                   scraper.stack_price,
                                   scraper.single_frequency,
                                   scraper.stack_frequency)
        else:
            scraper = AuctionScraper(item_id)
            cls.add_auction(item_id, scraper.single_price, scraper.stack_price,
                            scraper.single_frequency, scraper.stack_frequency)
            auction = cls.get_auction(item_id)

        return auction

    @classmethod
    def add_auction(cls, item_id, single_price, stack_price, single_frequency,
                    stack_frequency):
        cls.db.add_auction(item_id, single_price, stack_price,
                           single_frequency, stack_frequency)

    @classmethod
    def update_auction(cls, item_id, single_price, stack_price,
                       single_frequency, stack_frequency):
        cls.db.update_auction(item_id, single_price, stack_price,
                              single_frequency, stack_frequency)
