from controllers.auction_controller import AuctionController


class Product:
    def __init__(self, synth, item_id, quantity, cost=None, sell_price=None,
                 profit=None, sell_frequency=None) -> None:
        self.synth = synth
        self.item_id = item_id
        self.quantity = quantity

        if all(i is not None for i in [cost, sell_price, profit,
                                       sell_frequency]):
            self.cost = round(cost, 2)
            self.sell_price = round(sell_price, 2)
            self.profit = round(profit, 2)
            self.sell_frequency = round(sell_frequency, 2)
        else:
            self.cost, self.sell_price, self.profit, self.sell_frequency = \
                self.calculate_stats()

    def calculate_stats(self):
        """Returns the product cost, sell price, profit, and sell frequency"""
        # A dictionary containing all of the results from simulating the synth
        # several times
        # key: result item id, value: quantity
        results = self.synth.simulate()

        # The total cost is the cost of a single synth * the number of times
        # the synth was simulated
        simulation_cost = self.synth.cost * self.synth.num_trials

        # The total amount of the product made in the simulation, taking into
        # account the target quantity. If the product is a stack, this is the
        # number of stacks
        product_quantity = results[self.item_id] / self.quantity

        # The total cost of the simulation / the amount of product made in the
        # simulation = the cost to make each product
        cost = simulation_cost / product_quantity

        auction_stats = AuctionController.get_auction_stats(self.item_id)

        if self.quantity == 1:
            sell_price = auction_stats.average_single_price
            sell_frequency = auction_stats.average_single_frequency
        else:
            sell_price = auction_stats.average_stack_price
            sell_frequency = auction_stats.average_stack_frequency

        if sell_price is None:
            sell_price = 0

            # The total gil from the products made in the simulation
        simulation_product_gil = sell_price * product_quantity

        # The total profit made if all the simulation products were sold
        simulation_profit = simulation_product_gil - simulation_cost

        # The profit made per product
        profit = simulation_profit / product_quantity

        return round(cost, 2), round(sell_price, 2), round(profit, 2), \
            round(sell_frequency, 2)
