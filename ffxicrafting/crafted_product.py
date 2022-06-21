from collections import defaultdict
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

            nq_item = ItemController.get_item(recipe.result)

            # Result item cannot be sold on AH
            if nq_item.ah == 0:
                continue

            nq, hq1, hq2, hq3 = crafter.get_outcome_chances(recipe)

            # Multiply the quantity of the quality tier by the chance of that
            # quality tier to get an "expected quantity" for each tier
            nq_qty = recipe.result_qty * nq
            hq1_qty = recipe.result_hq1_qty * hq1
            hq2_qty = recipe.result_hq2_qty * hq2
            hq3_qty = recipe.result_hq3_qty * hq3

            # Since multiple quality tiers can produce the same item, need to
            # add together the quantities where the result item is the same
            # dict key = result item id, value = expected quantity per synth
            quantities = defaultdict(lambda: 0)
            quantities[recipe.result] += nq_qty
            quantities[recipe.result_hq1] += hq1_qty
            quantities[recipe.result_hq2] += hq2_qty
            quantities[recipe.result_hq3] += hq3_qty

            synth_cost = crafter.calculate_synth_cost(recipe)

            for item_id in quantities:
                item = ItemController.get_item(item_id)
                item_name = item.sort_name.replace("_", " ").title()
                quantity = quantities[item_id]
                single_cost = synth_cost / quantity
                stack_cost = single_cost * item.stack_size

                auction = AuctionController.get_auction(item_id)

                if auction.single_price is not None:
                    single_product = cls(recipe.id, item_name, 1,
                                         auction.single_price,
                                         auction.single_frequency, single_cost)
                    products.append(single_product)

                if auction.stack_price is not None:
                    stack_product = cls(recipe.id, item_name, item.stack_size,
                                        auction.stack_price,
                                        auction.stack_frequency, stack_cost)
                    products.append(stack_product)

        # Sort by value (function of profit and sell frequency)
        products.sort(key=lambda x: x.value, reverse=True)

        filtered_products = cls.filter_products(products, profit, frequency,
                                                value)
        return filtered_products
