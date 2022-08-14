class AuctionStats:
    def __init__(self, auction_pages) -> None:
        # Make sure all auction pages belong to the same item
        self.item_id = auction_pages[0].item_id
        if not all(i.item_id == self.item_id for i in auction_pages):
            raise ValueError("Multiple item ids found in auction pages")

        self.auction_pages = auction_pages

        averages = self.calculate_averages()
        self.average_single_price = averages[0]
        self.average_single_frequency = averages[1]
        self.average_stack_price = averages[2]
        self.average_stack_frequency = averages[3]

        self.single_sells_faster = (self.average_single_frequency is not None
                                    and self.average_stack_frequency is None
                                    or self.average_single_frequency is not None
                                    and self.average_stack_frequency is not None
                                    and self.average_single_frequency >
                                    self.average_stack_frequency)

        self.stack_sells_faster = (self.average_single_frequency is None
                                   and self.average_stack_frequency is not None
                                   or self.average_single_frequency is not None
                                   and self.average_stack_frequency is not None
                                   and self.average_single_frequency <=
                                   self.average_stack_frequency)

        self.no_sales = (self.average_single_price is None and
                         self.average_stack_price is None)

    def calculate_averages(self):
        single_price_averages = []
        single_frequencies = []
        stack_price_averages = []
        stack_frequencies = []

        for page in self.auction_pages:
            if page.single_sales > 0:
                single_price_average = page.single_price_sum / page.single_sales
                single_frequency = page.single_sales / page.num_days
            else:
                single_price_average = None
                single_frequency = None

            if page.stack_sales > 0:
                stack_price_average = page.stack_price_sum / page.stack_sales
                stack_frequency = page.stack_sales / page.num_days
            else:
                stack_price_average = None
                stack_frequency = None

            if single_price_average is not None:
                single_price_averages.append(single_price_average)
                single_frequencies.append(single_frequency)

            if stack_price_average is not None:
                stack_price_averages.append(stack_price_average)
                stack_frequencies.append(stack_frequency)

        if len(single_price_averages) > 0:
            overall_single_price_average = (sum(single_price_averages) /
                                            len(single_price_averages))
        else:
            overall_single_price_average = None

        if len(single_frequencies) > 0:
            single_frequency_average = (sum(single_frequencies) /
                                        len(single_frequencies))
        else:
            single_frequency_average = None

        if len(stack_price_averages) > 0:
            overall_stack_price_average = (sum(stack_price_averages) /
                                           len(stack_price_averages))
        else:
            overall_stack_price_average = None

        if len(stack_frequencies) > 0:
            stack_frequency_average = (sum(stack_frequencies) /
                                       len(stack_frequencies))
        else:
            stack_frequency_average = None

        return overall_single_price_average, single_frequency_average, \
            overall_stack_price_average, stack_frequency_average
