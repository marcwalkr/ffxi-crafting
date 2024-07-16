class AuctionItem:
    def __init__(self, id, item_id, avg_price, num_sales, sell_freq, is_stack, new_data, no_sale) -> None:
        self.id = id
        self.item_id = item_id
        self.avg_price = avg_price
        self.num_sales = num_sales
        self.sell_freq = sell_freq
        self.is_stack = is_stack
        self.new_data = new_data
        self.no_sale = no_sale
