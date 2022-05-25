class AuctionListing:
    def __init__(self, item_id, item_name, is_stack, price, sell_frequency) -> None:
        self.item_id = item_id
        self.item_name = item_name
        self.is_stack = is_stack
        self.price = price
        self.sell_frequency = sell_frequency

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
