import statistics
from database import Database
from models import AuctionItem, SalesHistory


class AuctionController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_auction_item(cls, item_id, is_stack):
        auction_item_tuple = cls.db.get_auction_item(item_id, is_stack)
        if auction_item_tuple is not None:
            auction_item = AuctionItem(*auction_item_tuple)
            if auction_item.new_data:
                sales_history = cls.get_latest_sales_history(item_id, is_stack)

                prices = [sale.price for sale in sales_history]
                avg_price = sum(prices) / len(prices)

                # Update attributes of the auction_item object
                auction_item.avg_price = avg_price
                auction_item.sell_freq = auction_item.num_sales / 15

                cls.update_auction_item(item_id, avg_price, auction_item.sell_freq, is_stack)

            return auction_item
        else:
            return None

    @classmethod
    def update_auction_item(cls, item_id, avg_price, sell_freq, is_stack):
        cls.db.update_auction_item(item_id, avg_price, sell_freq, is_stack)

    @classmethod
    def get_latest_sales_history(cls, item_id, is_stack):
        sales_history_tuples = cls.db.get_latest_sales_history(item_id, is_stack)
        if sales_history_tuples:
            sales_history_list = [SalesHistory(*sales_history_tuple) for sales_history_tuple in sales_history_tuples]
            return sales_history_list
        else:
            return []
