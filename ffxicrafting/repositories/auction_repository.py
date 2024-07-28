from models import AuctionItem, SalesHistory


class AuctionRepository:
    cache = {}

    def __init__(self, db) -> None:
        self.db = db

    def get_auction_items(self, item_id):
        if item_id in self.cache:
            return self.cache[item_id]
        else:
            auction_item_tuples = self.db.get_auction_items(item_id)
            if auction_item_tuples is not None:
                auction_items = [AuctionItem(*auction_item_tuple) for auction_item_tuple in auction_item_tuples]
                for auction_item in auction_items:
                    if auction_item.new_data:
                        sales_history = self.get_latest_sales_history(item_id, auction_item.is_stack)

                        if not sales_history:
                            continue

                        prices = [sale.price for sale in sales_history]
                        avg_price = sum(prices) / len(prices)
                        auction_item.avg_price = avg_price
                        auction_item.sell_freq = auction_item.num_sales / 15

                        self.update_auction_item(item_id, avg_price, auction_item.sell_freq, auction_item.is_stack)

                self.cache[item_id] = auction_items
                return auction_items
            else:
                self.cache[item_id] = []
                return []

    def update_auction_item(self, item_id, avg_price, sell_freq, is_stack):
        self.db.update_auction_item(item_id, avg_price, sell_freq, is_stack)

    def get_latest_sales_history(self, item_id, is_stack):
        sales_history_tuples = self.db.get_latest_sales_history(item_id, is_stack)
        if sales_history_tuples:
            sales_history_list = [SalesHistory(*sales_history_tuple) for sales_history_tuple in sales_history_tuples]
            return sales_history_list
        else:
            return []
