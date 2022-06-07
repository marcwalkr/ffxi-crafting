class Auction:
    def __init__(self, item_id, single_price, stack_price, single_frequency,
                 stack_frequency) -> None:
        self.item_id = item_id
        self.single_price = single_price
        self.stack_price = stack_price
        self.single_frequency = single_frequency
        self.stack_frequency = stack_frequency
