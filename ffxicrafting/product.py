from controllers.synth_controller import SynthController
from controllers.auction_controller import AuctionController
from controllers.item_controller import ItemController
from config import Config


class Product:
    def __init__(self, recipe_id, item_name, quantity, sell_price,
                 sell_frequency, cost) -> None:
        self.recipe_id = recipe_id
        self.item_name = item_name
        self.quantity = quantity
        self.sell_price = sell_price
        self.sell_frequency = sell_frequency
        self.cost = cost
        self.profit = sell_price - cost
        self.value = (self.profit * sell_frequency) / 1000

    @classmethod
    def get_products(cls, crafter, profit, frequency, value):
        products = []
        recipes = SynthController.get_recipes(crafter.skill_set)

        for recipe in recipes:
            requres_key_item = recipe.key_item > 0
            if requres_key_item and recipe.key_item not in crafter.key_items:
                continue

            include_desynth = Config.get_include_desynth()
            if recipe.desynth and not include_desynth:
                continue

            # TODO: handle HQ results
            result_item = ItemController.get_item(recipe.result)

            # Result item cannot be sold on AH
            if result_item.ah == 0:
                continue

            synth_cost = crafter.calculate_synth_cost(recipe)
            single_cost = synth_cost / recipe.result_qty
            stack_cost = single_cost * result_item.stack_size

            auction = AuctionController.get_auction(recipe.result)

            if auction.single_price is not None:
                single_product = cls(recipe.id, recipe.result_name, 1,
                                     auction.single_price,
                                     auction.single_frequency, single_cost)
                products.append(single_product)

            if auction.stack_price is not None:
                stack_product = cls(recipe.id, recipe.result_name,
                                    result_item.stack_size,
                                    auction.stack_price,
                                    auction.stack_frequency, stack_cost)
                products.append(stack_product)

        # Sort by value (function of profit and sell frequency)
        products.sort(key=lambda x: x.value, reverse=True)

        filtered_products = cls.filter_products(products, profit, frequency,
                                                value)
        return filtered_products

    @staticmethod
    def filter_products(products, profit_threshold, freq_threshold,
                        value_threshold):
        """Removes duplicates from different recipes that are less profitable
        and any that don't pass thresholds
        """
        filtered = []
        for product in products:
            duplicate = any(x.item_name == product.item_name and
                            x.quantity == product.quantity for x in filtered)
            profitable = product.profit >= profit_threshold
            fast_selling = product.sell_frequency >= freq_threshold
            valuable = product.value >= value_threshold

            if profitable and fast_selling and valuable and not duplicate:
                filtered.append(product)

        return filtered
