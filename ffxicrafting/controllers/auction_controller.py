from database import Database
from models.auction_item import AuctionItem


class AuctionController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_auction_item(cls, item_id):
        auction_item_tuple = cls.db.get_auction_item(item_id)

        if auction_item_tuple is not None:
            return AuctionItem(*auction_item_tuple)
        else:
            return None

    @classmethod
    def add_auction_item(cls, item_id, avg_single_price, avg_stack_price, sales_frequency):
        cls.db.add_auction_item(item_id, avg_single_price, avg_stack_price, sales_frequency)

    @classmethod
    def delete_auction_items(cls):
        cls.db.delete_auction_items()
