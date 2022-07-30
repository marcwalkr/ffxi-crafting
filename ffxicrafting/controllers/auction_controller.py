from database import Database
from helpers import get_current_timestamp
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

        else:
            scraper = AuctionScraper(item_id)
            cls.add_auction(item_id, scraper.single_sales,
                            scraper.single_price_sum, scraper.stack_sales,
                            scraper.stack_price_sum, scraper.days)
            auction = cls.get_auction(item_id)

        return auction

    @classmethod
    def add_auction(cls, item_id, single_sales, single_price_sum, stack_sales,
                    stack_price_sum, days):
        cls.db.add_auction(item_id, single_sales, single_price_sum,
                           stack_sales, stack_price_sum, days)

    @classmethod
    def update_auction(cls, item_id, single_sales, single_price_sum,
                       stack_sales, stack_price_sum, days, timestamp):
        cls.db.update_auction(item_id, single_sales, single_price_sum,
                              stack_sales, stack_price_sum, days, timestamp)

    @classmethod
    def update_all_auctions(cls):
        auction_tuples = cls.db.get_all_auctions()

        for auction_tuple in auction_tuples:
            item_id = auction_tuple[0]
            scraper = AuctionScraper(item_id)
            timestamp = get_current_timestamp()
            cls.update_auction(item_id, scraper.single_sales,
                               scraper.single_price_sum,
                               scraper.stack_sales,
                               scraper.stack_price_sum, scraper.days,
                               timestamp)
