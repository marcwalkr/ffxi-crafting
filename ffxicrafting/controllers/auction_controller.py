from database import Database
from models.auction import Auction


class AuctionController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_auction(cls, item_id):
        auction_tuple = cls.db.get_auction(item_id)

        if auction_tuple is not None:
            return Auction(*auction_tuple)
        else:
            return None

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
