from product import Product
from config import Config
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from controllers.auction_controller import AuctionController


class CraftedProduct(Product):
    def __init__(self, recipe_id, item_name, quantity, sell_price,
                 sell_frequency, cost) -> None:
        super().__init__(item_name, quantity, sell_price, sell_frequency, cost)
        self.recipe_id = recipe_id

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
