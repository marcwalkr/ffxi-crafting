from database import Database
from helpers import sort_alphabetically
from auction_scraper import AuctionScraper


class AuctionListing:
    db = Database()

    def __init__(self, name, quantity, price, sell_freq) -> None:
        self.name = name
        self.quantity = quantity
        self.price = price
        self.sell_freq = sell_freq

        if quantity > 1:
            self.single_price = price / quantity
        else:
            self.single_price = price

    def add_to_database(self):
        self.db.add_auction_listing(self)

    @classmethod
    def update_ah_data(cls):
        """Clears and repopulates the auction listing table, refreshing all data"""
        cls.db.delete_all_auction_listings()

        all_items = cls.db.get_all_items()
        for item in all_items:
            item_name, stack_quantity = item[0:2]
            listings = cls.scrape_listings(item_name, stack_quantity)

            for listing in listings:
                listing.add_to_database()

    @classmethod
    def get_all_listings(cls):
        all_listings = []
        all_listing_tuples = cls.db.get_all_auction_listings()
        for listing_tuple in all_listing_tuples:
            listing = cls(*listing_tuple)
            all_listings.append(listing)

        sorted = sort_alphabetically(all_listings)

        return sorted

    @classmethod
    def remove_listings(cls, name):
        cls.db.remove_auction_listings(name)

    @classmethod
    def scrape_listings(cls, item_name, stack_quantity):
        scraper = AuctionScraper(item_name)
        scraper.scrape()

        single_price = scraper.get_single_price()
        single_freq = scraper.get_single_freq()

        stack_price = scraper.get_stack_price()
        stack_freq = scraper.get_stack_freq()

        listings = []

        if single_price is not None:
            single_listing = AuctionListing(item_name, 1, single_price,
                                            single_freq)
            listings.append(single_listing)

        if stack_price is not None:
            stack_listing = AuctionListing(item_name, stack_quantity,
                                           stack_price, stack_freq)
            listings.append(stack_listing)

        return listings
