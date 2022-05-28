from result_controller import ResultController
from recipe_controller import RecipeController
from auction_controller import AuctionController
from item_controller import ItemController


class Product:
    def __init__(self, item_name, quantity, sell_price, sell_frequency,
                 cost) -> None:
        self.item_name = item_name
        self.quantity = quantity
        self.sell_price = sell_price
        self.sell_frequency = sell_frequency
        self.cost = cost
        self.profit = sell_price - cost

    @classmethod
    def get_products(cls, profit_threshold, freq_threshold):
        # Get all synthesis results
        synth_results = ResultController.get_all_results()

        products = []

        for result in synth_results:
            # For now, skip HQ qualities
            # TODO: calculate cost and profit factoring in HQ and craft skill
            if result.quality_level != "NQ":
                continue

            # Get the recipe for the result by recipe id
            recipe = RecipeController.get_recipe_by_id(result.recipe_id)
            # Calculate the cost of one synth
            synth_cost = RecipeController.calculate_synth_cost(recipe)
            # The cost to craft one of the item
            single_cost = synth_cost / result.quantity
            # Get the auction data for the item
            auction_item = AuctionController.get_auction_item(result.item_name)
            # Get the item for the stack quantity
            item = ItemController.get_item(result.item_name)
            # The cost to craft a stack of the item
            stack_cost = single_cost * item.stack_quantity

            if auction_item.single_price is not None:
                single_product = cls(item.name, 1, auction_item.single_price,
                                     auction_item.single_frequency,
                                     single_cost)
                products.append(single_product)

            if auction_item.stack_price is not None:
                stack_product = cls(item.name, item.stack_quantity,
                                    auction_item.stack_price,
                                    auction_item.stack_frequency, stack_cost)
                products.append(stack_product)

        products = cls.filter_threshold(products, profit_threshold,
                                        freq_threshold)
        profit_sorted = sorted(products, key=lambda x: x.profit, reverse=True)

        return profit_sorted

    @staticmethod
    def filter_threshold(products, profit_threshold, freq_threshold):
        filtered = []
        for product in products:
            profitable = product.profit >= profit_threshold
            fast_selling = product.sell_frequency >= freq_threshold

            if profitable and fast_selling:
                filtered.append(product)

        return filtered
