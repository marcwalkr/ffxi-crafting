from database import Database


class AuctionListing:
    db = Database()

    def __init__(self, item_name, is_stack, price, sell_frequency) -> None:
        self.item_name = item_name
        self.is_stack = is_stack
        self.price = price
        self.sell_frequency = sell_frequency

    def to_database(self):
        self.db.add_auction_listing(self)

    # @classmethod
    # def update_ah_data(cls):
    #     """Clears and repopulates the auction listing table, refreshing all data"""
    #     cls.db.delete_all_auction_listings()

    #     all_items = cls.db.get_all_items()
    #     for item in all_items:
    #         item_name, stack_quantity = item[0:2]
    #         listings = cls.scrape_listings(item_name, stack_quantity)

    #         for listing in listings:
    #             listing.add_to_database()

    # @classmethod
    # def get_all_listings(cls):
    #     all_listings = []
    #     all_listing_tuples = cls.db.get_all_auction_listings()
    #     for listing_tuple in all_listing_tuples:
    #         listing = cls(*listing_tuple)
    #         all_listings.append(listing)

    #     sorted = sort_alphabetically(all_listings)

    #     return sorted

    # @classmethod
    # def get_listings(cls, name):
    #     listings = []
    #     listing_tuples = cls.db.get_auction_listings(name)
    #     for listing_tuple in listing_tuples:
    #         listing = cls(*listing_tuple)
    #         listings.append(listing)

    #     return listings

    # @classmethod
    # def remove_listings(cls, name):
    #     cls.db.remove_auction_listings(name)

    # @classmethod
    # def is_in_database(cls, name):
    #     return cls.db.auction_listing_is_in_database(name)
