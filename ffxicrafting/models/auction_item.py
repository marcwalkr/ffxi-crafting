class AuctionItem:
    def __init__(self, item_id, avg_single_price, avg_stack_price, sales_frequency) -> None:
        self.item_id = item_id
        self.avg_single_price = avg_single_price
        self.avg_stack_price = avg_stack_price
        self.sales_frequency = sales_frequency
