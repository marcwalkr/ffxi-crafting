from synth import Synth
from config import Config
from controllers.auction_controller import AuctionController


class Product:
    def __init__(self, recipe, crafter, item_id, quantity) -> None:
        if item_id not in [recipe.result, recipe.result_hq1, recipe.result_hq2,
                           recipe.result_hq3]:
            raise ValueError("Product cannot be crafted from recipe")

        self.synth = Synth(recipe, crafter)
        self.synth.cost = self.synth.calculate_cost()
        self.item_id = item_id
        self.quantity = quantity

        self.cost, self.product_profit, self.total_profit, \
            self.sell_frequency = self.calculate_cost_profits_frequency()

    def calculate_cost_profits_frequency(self):
        # An ingredient price could not be found
        if self.synth.cost is None:
            return None, None, None, None

        # A dictionary containing all of the results from simulating the synth
        # several times
        # key: result item id, value: quantity
        results = self.synth.simulate()

        # The total cost is the cost of a single synth * the number of times
        # the synth was simulated
        total_cost = self.synth.cost * self.synth.num_trials

        # The total amount of the product made in the simulation
        product_quantity = results[self.item_id] / self.quantity

        # The total cost of the simulation / the amount of product made in the
        # simulation = the cost to make each product
        product_cost = total_cost / product_quantity

        product_gil_sum = 0
        other_gil_sum = 0
        sell_frequency = 0
        for item_id, quantity in results.items():
            auction_stats = AuctionController.get_auction_stats(item_id)

            # This result is the target product, calculate gil using the
            # product quantity rather than the individual quantity
            if item_id == self.item_id:
                gil = self.calculate_product_gil(auction_stats,
                                                 product_quantity)
                if gil is not None:
                    product_gil_sum += gil
                    # The product frequency is the only one needed, don't need the
                    # frequency of other results
                    if self.quantity == 1:
                        sell_frequency = auction_stats.average_single_frequency
                    else:
                        sell_frequency = auction_stats.average_stack_frequency
            else:
                # Not the target product, but interested in the gil sum
                gil = self.synth.calculate_gil(auction_stats, quantity)
                if gil is not None:
                    other_gil_sum += gil

        # The profit made per product if only selling the product, not any
        # other results crafted while crafting the product
        product_profit = (product_gil_sum - total_cost) / product_quantity

        # The profit made per product if selling everything made in the process
        # of crafting the product
        total_gil_sum = product_gil_sum + other_gil_sum
        total_profit = (total_gil_sum - total_cost) / product_quantity

        return round(product_cost, 2), round(product_profit, 2), \
            round(total_profit, 2), round(sell_frequency, 2)

    def calculate_product_gil(self, auction_stats, product_quantity):
        """Returns the total amount of gil a quantity of a product is worth.
        If the product is a stack, the product_quantity is the number of
        stacks"""
        if self.quantity == 1:
            price = auction_stats.average_single_price
        else:
            price = auction_stats.average_stack_price

        if price is None:
            return None

        return price * product_quantity
