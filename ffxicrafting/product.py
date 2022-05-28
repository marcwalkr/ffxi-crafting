from synth_controller import SynthController
from auction_controller import AuctionController
from item_controller import ItemController
from vendor_controller import VendorController


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
        synth_results = SynthController.get_all_results()

        products = []

        for result in synth_results:
            # For now, skip HQ qualities
            # TODO: calculate cost and profit factoring in HQ and craft skill
            if result.quality_level != "NQ":
                continue

            # Get the recipe for the result by recipe id
            recipe = SynthController.get_recipe_by_id(result.recipe_id)
            # Calculate the cost of one synth
            synth_cost = cls.calculate_synth_cost(recipe)
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

    @classmethod
    def calculate_synth_cost(cls, recipe):
        cost = 0

        for ingredient in [recipe.crystal] + recipe.ingredients:
            # Look for every method of obtaining the single ingredient
            # (auction, vendor, craft)
            prices = []

            # Get the auction item for the ingredient
            auction_item = AuctionController.get_auction_item(ingredient)

            # Get the item for the stack quantity
            item = ItemController.get_item(ingredient)

            # Append both prices for one
            # single_price and (stack_price / stack_quantity)
            if auction_item.single_price is not None:
                prices.append(auction_item.single_price)

            if auction_item.stack_price is not None:
                single_from_stack = auction_item.stack_price / item.stack_quantity
                prices.append(single_from_stack)

            # Get all vendor items for the ingredient
            vendor_items = VendorController.get_vendor_items(ingredient)
            if len(vendor_items) > 0:
                # Append all of the prices
                for vendor_item in vendor_items:
                    prices.append(vendor_item.price)

            # Find the cost to craft the single ingredient
            synth_results = SynthController.get_results(ingredient)
            for result in synth_results:
                # For now, skip HQ qualities
                # TODO: calculate the cost factoring in HQ and craft skill
                if result.quality_level != "NQ":
                    continue

                result_recipe = cls.get_recipe_by_id(result.recipe_id)
                result_synth_cost = result_recipe.calculate_synth_cost()
                ingredient_cost = result_synth_cost / result.quantity
                prices.append(ingredient_cost)

            # Add the min price (cheapest way to obtain the item) to the cost
            cheapest = min(prices)
            cost += cheapest

        return cost

    @staticmethod
    def filter_threshold(products, profit_threshold, freq_threshold):
        filtered = []
        for product in products:
            profitable = product.profit >= profit_threshold
            fast_selling = product.sell_frequency >= freq_threshold

            if profitable and fast_selling:
                filtered.append(product)

        return filtered
