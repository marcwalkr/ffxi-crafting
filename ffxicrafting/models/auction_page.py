class AuctionPage:
    def __init__(self, item_id, single_sales, single_price_sum, stack_sales,
                 stack_price_sum, num_days, accessed) -> None:
        self.item_id = item_id
        self.single_sales = single_sales
        self.single_price_sum = single_price_sum
        self.stack_sales = stack_sales
        self.stack_price_sum = stack_price_sum
        self.num_days = num_days
        self.accessed = accessed
