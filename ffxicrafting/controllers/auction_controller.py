from database import Database
from helpers import get_utc_timestamp
from models.auction_page import AuctionPage
from auction_stats import AuctionStats
from controllers.item_controller import ItemController
from auction_scraper import AuctionScraper


class AuctionController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_auction_stats(cls, item_id):
        auction_pages = cls.get_auction_pages(item_id)
        auction_stats = AuctionStats(auction_pages)
        return auction_stats

    @classmethod
    def get_auction_pages(cls, item_id):
        page_tuples = cls.db.get_auction_pages(item_id)

        if len(page_tuples) > 0:
            auction_pages = []
            for page_tuple in page_tuples:
                auction_page = AuctionPage(*page_tuple)
                auction_pages.append(auction_page)
        else:
            cls.scrape_add_auction_page(item_id)
            auction_pages = cls.get_auction_pages(item_id)

        return auction_pages

    @classmethod
    def get_all_auction_pages(cls):
        page_tuples = cls.db.get_all_auction_pages()

        auction_pages = []
        for page_tuple in page_tuples:
            auction_page = AuctionPage(*page_tuple)
            auction_pages.append(auction_page)

        return auction_pages

    @classmethod
    def scrape_add_auction_page(cls, item_id):
        scraper = AuctionScraper(item_id)
        accessed = get_utc_timestamp()
        cls.db.add_auction_page(item_id, scraper.single_sales,
                                scraper.single_price_sum, scraper.stack_sales,
                                scraper.stack_price_sum, scraper.num_days,
                                accessed)

    @classmethod
    def update_auction_data(cls):
        all_auction_pages = cls.get_all_auction_pages()

        item_ids = []
        for auction_page in all_auction_pages:
            item_ids.append(auction_page.item_id)

        # Remove duplicates
        item_ids = [*set(item_ids)]

        cls.db.delete_auction_pages_older_than(90)

        for item_id in item_ids:
            item = ItemController.get_item(item_id)

            # Item cannot be sold on AH
            if item.ah == 0:
                continue

            cls.scrape_add_auction_page(item_id)
