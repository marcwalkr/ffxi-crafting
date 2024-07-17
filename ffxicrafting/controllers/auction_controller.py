from database.database import Database
from models.auction_item import AuctionItem
from models.sales_history import SalesHistory


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
                unix_timestamps = [sale.sell_date for sale in sales_history]
                # Ensure the timestamps are sorted
                unix_timestamps.sort()

                # Calculate the differences between consecutive timestamps
                time_diffs = [unix_timestamps[i] - unix_timestamps[i-1] for i in range(1, len(unix_timestamps))]

                if len(time_diffs) <= 1:
                    sales_per_day = 0
                else:
                    # Calculate the average time between sales
                    avg_interval_seconds = sum(time_diffs) / len(time_diffs)

                    # Estimate sales per day
                    sales_per_day = (24 * 60 * 60) / avg_interval_seconds

                prices = [sale.price for sale in sales_history]
                avg_price = sum(prices) / len(prices)

                # Update the attributes of the auction_item object
                auction_item.avg_price = avg_price
                auction_item.num_sales = len(sales_history)
                auction_item.sell_freq = sales_per_day

                cls.update_auction_item(item_id, avg_price, len(sales_history), sales_per_day, is_stack)

            return auction_item
        else:
            return None

    @classmethod
    def update_auction_item(cls, item_id, avg_price, num_sales, sell_freq, is_stack):
        cls.db.update_auction_item(item_id, avg_price, num_sales, sell_freq, is_stack)

    @classmethod
    def get_latest_sales_history(cls, item_id, is_stack):
        sales_history_tuples = cls.db.get_latest_sales_history(item_id, is_stack)
        if sales_history_tuples:
            sales_history_list = [SalesHistory(*sales_history_tuple) for sales_history_tuple in sales_history_tuples]
            return sales_history_list
        else:
            return []
