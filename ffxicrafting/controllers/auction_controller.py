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
                unix_timestamps = [sale.sell_date for sale in sales_history]

                if len(unix_timestamps) < 15:
                    # Less than 15 have ever been sold
                    sales_per_day = 0
                else:
                    # Ensure the timestamps are sorted
                    unix_timestamps.sort()

                    # Calculate the differences between consecutive timestamps
                    time_diffs = [unix_timestamps[i] - unix_timestamps[i-1] for i in range(1, len(unix_timestamps))]

                    # Filter out differences less than 30 seconds
                    time_diffs = [diff for diff in time_diffs if diff > 30]

                    if len(time_diffs) == 0:
                        # Every item sold fast, set to 9999 as maximum
                        sales_per_day = 9999
                    else:
                        # Calculate the median time between sales
                        median_interval_seconds = statistics.median(time_diffs)

                        # Estimate sales per day
                        sales_per_day = (24 * 60 * 60) / median_interval_seconds

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
