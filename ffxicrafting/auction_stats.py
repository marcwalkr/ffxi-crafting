from config import Config


class AuctionStats:
    def __init__(self, item_name) -> None:
        single_price, stack_price = Config.get_auction_prices(item_name)

        if single_price > 0:
            self.single_price = single_price
        else:
            self.single_price = None

        if stack_price > 0:
            self.stack_price = stack_price
        else:
            self.stack_price = None

        self.single_frequency, self.stack_frequency = \
            Config.get_sell_frequencies(item_name)

        self.single_sells_faster = (self.single_frequency > 0
                                    and self.stack_frequency == 0
                                    or self.single_frequency > 0
                                    and self.stack_frequency > 0
                                    and self.single_frequency >
                                    self.stack_frequency)

        self.stack_sells_faster = (self.single_frequency == 0
                                   and self.stack_frequency > 0
                                   or self.single_frequency > 0
                                   and self.stack_frequency > 0
                                   and self.single_frequency <=
                                   self.stack_frequency)

        self.no_sales = (self.single_price is None and
                         self.stack_price is None)
