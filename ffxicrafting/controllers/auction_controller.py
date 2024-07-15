from functools import lru_cache
from database.database import Database
from models.auction_item import AuctionItem


class AuctionController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    @lru_cache(maxsize=None)
    def get_auction_item(cls, item_id):
        auction_item_tuple = cls.db.get_auction_item(item_id)

        if auction_item_tuple is not None:
            return AuctionItem(*auction_item_tuple)
        else:
            return None

    @classmethod
    def auction_item_exists(cls, item_id):
        return cls.get_auction_item(item_id) is not None

    @classmethod
    def add_auction_item(cls, item_id, single_price, stack_price):
        cls.db.add_auction_item(item_id, single_price, stack_price)
        # Invalidate the cache for this item_id
        cls.get_auction_item.cache_clear()

    @classmethod
    def update_auction_item(cls, item_id, single_price, stack_price):
        cls.db.update_auction_item(item_id, single_price, stack_price)
        # Invalidate the cache for this item_id
        cls.get_auction_item.cache_clear()

    @classmethod
    def delete_auction_items(cls):
        cls.db.delete_auction_items()
        # Invalidate the entire cache
        cls.get_auction_item.cache_clear()
