from models import AuctionItem, SalesHistory


class AuctionRepository:
    def __init__(self, db) -> None:
        self.db = db
        self.cache = {}

    def get_auction_items(self, item_id):
        if item_id in self.cache:
            return self.cache[item_id]
        else:
            auction_item_tuples = self.db.get_auction_items(item_id)
            if auction_item_tuples is not None:
                auction_items = [AuctionItem(*auction_item_tuple) for auction_item_tuple in auction_item_tuples]
                self.cache[item_id] = auction_items
                return auction_items
            else:
                self.cache[item_id] = []
                return []

    def update_auction_item(self, new_item):
        self.db.update_auction_item(new_item.item_id, new_item.avg_price, new_item.sell_freq, new_item.is_stack)
        self.cache[new_item.item_id] = new_item

    def get_latest_sales_history(self, item_id, is_stack):
        sales_history_tuples = self.db.get_latest_sales_history(item_id, is_stack)
        if sales_history_tuples:
            sales_history_list = [SalesHistory(*sales_history_tuple) for sales_history_tuple in sales_history_tuples]
            return sales_history_list
        else:
            return []
