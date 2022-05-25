class AuctionData:
    def __init__(self, item_id, item_name, single_price, single_frequency,
                 stack_price, stack_frequency) -> None:
        self.item_id = item_id
        self.item_name = item_name
        self.single_price = single_price
        self.single_frequency = single_frequency
        self.stack_price = stack_price
        self.stack_frequency = stack_frequency
