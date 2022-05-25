from database import Database
from auction_listing import AuctionListing


class AuctionListingController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def add_auction_listings(cls, auction_data):

        if auction_data.single_price is not None:
            single_listing = AuctionListing(auction_data.item_id,
                                            auction_data.item_name, False,
                                            auction_data.single_price,
                                            auction_data.single_frequency)
            cls.db.add_auction_listing(single_listing)

        if auction_data.stack_price is not None:
            stack_listing = AuctionListing(auction_data.item_id,
                                           auction_data.item_name, True,
                                           auction_data.stack_price,
                                           auction_data.stack_frequency)
            cls.db.add_auction_listing(stack_listing)
