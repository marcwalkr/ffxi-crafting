from auction_scraper import AuctionScraper
from auction_data import AuctionData


class AuctionDataController:
    def __init__(self) -> None:
        pass

    @classmethod
    def get_auction_data(cls, item_name):
        scraper = AuctionScraper(item_name)

        if scraper.item_id is not None:
            data = AuctionData(scraper.item_id, scraper.item_name,
                               scraper.single_price, scraper.single_freq,
                               scraper.stack_price, scraper.stack_freq)
            return data
        else:
            return None
