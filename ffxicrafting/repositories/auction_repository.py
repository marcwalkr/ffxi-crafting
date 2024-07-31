from models import AuctionItem, SalesHistory
from functools import lru_cache


class AuctionRepository:
    def __init__(self, db) -> None:
        self.db = db

    @lru_cache(maxsize=None)
    def get_auction_items(self, item_id):
        auction_item_tuples = self.db.get_auction_items(item_id)
        if auction_item_tuples is not None:
            auction_items = [AuctionItem(*auction_item_tuple) for auction_item_tuple in auction_item_tuples]
            return auction_items
        else:
            return []

    def update_auction_item(self, new_item):
        self.db.update_auction_item(new_item.item_id, new_item.avg_price, new_item.sell_freq, new_item.is_stack)
        self.get_auction_items.cache_clear()

    def get_latest_sales_history(self, item_id, is_stack):
        sales_history_tuples = self.db.get_latest_sales_history(item_id, is_stack)
        if sales_history_tuples:
            sales_history_list = [SalesHistory(*sales_history_tuple) for sales_history_tuple in sales_history_tuples]
            return sales_history_list
        else:
            return []
