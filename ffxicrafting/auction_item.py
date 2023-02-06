class AuctionItem:
    def __init__(self, item_name, single_price, stack_price) -> None:
        self.item_name = item_name

        if single_price > 0:
            self.single_price = single_price
        else:
            self.single_price = None

        if stack_price > 0:
            self.stack_price = stack_price
        else:
            self.stack_price = None

        self.no_sales = self.single_price is None and self.stack_price is None
