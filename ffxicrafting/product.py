from controllers.item_controller import ItemController
from controllers.bundle_controller import BundleController
from ingredient import Ingredient
from auction_stats import AuctionStats


class Product:
    def __init__(self, synth, item_id, quantity, cost=None, sell_price=None,
                 profit=None, sell_frequency=None) -> None:

        self.synth = synth
        self.item_id = item_id
        self.quantity = quantity

        self.item = ItemController.get_item(item_id)
        self.name = self.item.sort_name.replace("_", " ").title()

        if all(i is not None for i in [cost, sell_price, profit,
                                       sell_frequency]):
            self.cost = round(cost, 2)
            self.sell_price = round(sell_price, 2)
            self.profit = round(profit, 2)
            self.sell_frequency = round(sell_frequency, 2)
        else:
            self.cost, self.sell_price, self.profit, self.sell_frequency = \
                self.calculate_stats()

        self.bundle = BundleController.get_bundle(item_id)
        if self.bundle is not None and quantity > 1:
            self.can_bundle = True
        else:
            self.can_bundle = False

    def calculate_stats(self):
        """Returns the product cost, sell price, profit, and sell frequency"""
        # A dictionary containing all of the results from simulating the synth
        # several times
        # key: result item id, value: quantity
        results, retained_ingredients = self.synth.simulate()

        # The total cost is the cost of a single synth * the number of times
        # the synth was simulated
        simulation_cost = self.synth.cost * self.synth.num_trials

        # Subtract the price of remaining ingredients from the cost
        saved_cost = 0
        for ingredient_id, amount in retained_ingredients.items():
            ingredient = Ingredient(ingredient_id)
            saved_cost += ingredient.price * amount

        simulation_cost -= saved_cost

        # The total amount of the product made in the simulation, taking into
        # account the target quantity. If the product is a stack, this is the
        # number of stacks
        product_quantity = results[self.item_id] / self.quantity

        # The total cost of the simulation / the amount of product made in the
        # simulation = the cost to make each product
        if product_quantity == 0:
            cost = simulation_cost
        else:
            cost = simulation_cost / product_quantity

        auction_stats = AuctionStats(self.item.name)

        if self.quantity == 1:
            sell_price = auction_stats.single_price
            sell_frequency = auction_stats.single_frequency
        else:
            sell_price = auction_stats.stack_price
            sell_frequency = auction_stats.stack_frequency

        if sell_price is None:
            sell_price = 0

            # The total gil from the products made in the simulation
        simulation_product_gil = sell_price * product_quantity

        # The total profit made if all the simulation products were sold
        simulation_profit = simulation_product_gil - simulation_cost

        # The profit made per product
        if product_quantity == 0:
            profit = simulation_profit
        else:
            profit = simulation_profit / product_quantity

        return round(cost, 2), round(sell_price, 2), round(profit, 2), \
            round(sell_frequency, 2)

    def create_bundle_products(self):
        bundle_item = ItemController.get_item(self.bundle.bundled_id)
        trade_item = Ingredient(self.bundle.trade_item_id)

        auction_stats = AuctionStats(bundle_item.name)

        if auction_stats.no_sales:
            return []

        single_bundled_cost = self.cost + trade_item.price

        products = []

        if auction_stats.single_price is not None:
            single_price = auction_stats.single_price
            profit = single_price - single_bundled_cost
            single_frequency = auction_stats.single_frequency
            single_product = Product(self.synth, bundle_item.item_id, 1,
                                     single_bundled_cost, single_price, profit,
                                     single_frequency)
            products.append(single_product)

        if auction_stats.stack_price is not None:
            stack_bundled_cost = single_bundled_cost * bundle_item.stack_size
            stack_price = auction_stats.stack_price
            profit = stack_price - stack_bundled_cost
            stack_frequency = auction_stats.stack_frequency
            stack_product = Product(self.synth, bundle_item.item_id,
                                    bundle_item.stack_size, stack_bundled_cost,
                                    stack_price, profit, stack_frequency)
            products.append(stack_product)

        return products
