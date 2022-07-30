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
    def get_products(cls, crafters, profit, frequency, sort_column):
        products = []
        skill_range = Config.get_skill_range()

        for crafter in crafters:
            recipes = SynthController.get_recipes(crafter.skill_set,
                                                  skill_range)

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

                    quantity = quantities[item_id]
                    single_cost = synth_cost / quantity
                    stack_cost = single_cost * item.stack_size

                    products += cls.create_products(recipe.id, item_id,
                                                    single_cost)

                    bundleable_names = ["arrow", "bolt", "bullet", "card"]
                    if any(x in item.name for x in bundleable_names):
                        products += cls.get_bundle_products(recipe.id,
                                                            item.name,
                                                            stack_cost)

        products = cls.filter_products(products, profit, frequency)
        products = cls.sort_products(products, sort_column)

        return products

    @classmethod
    def get_bundle_products(cls, recipe_id, item_name, unbundled_cost):
        if "arrow" in item_name:
            bundle_name = item_name.removesuffix("_arrow") + "_quiver"
        elif "bolt" in item_name:
            bundle_name = item_name + "_quiver"
        elif "bullet" in item_name:
            bundle_name = item_name + "_pouch"
        else:
            bundle_name = item_name + "_case"

        item = ItemController.get_item_by_name(bundle_name)

        if item is not None:
            item_id = item.item_id

            # A carnation costs 60 gil, required to bundle each stack
            bundled_cost = unbundled_cost + 60

            return cls.create_products(recipe_id, item_id, bundled_cost)
        else:
            return []

    @classmethod
    def create_products(cls, recipe_id, item_id, single_cost):
        item = ItemController.get_item(item_id)
        item_name = item.sort_name.replace("_", " ").title()

        auction = AuctionController.get_auction(item_id)

        products = []

        if auction.single_sales > 0:
            avg_single_price = auction.single_price_sum / auction.single_sales
            avg_single_frequency = auction.single_sales / auction.days

            single_product = cls(recipe_id, item_name, 1,
                                 avg_single_price, avg_single_frequency,
                                 single_cost)
            products.append(single_product)

        if auction.stack_sales > 0:
            avg_stack_price = auction.stack_price_sum / auction.stack_sales
            avg_stack_frequency = auction.stack_sales / auction.days

            stack_cost = single_cost * item.stack_size
            stack_product = cls(recipe_id, item_name, item.stack_size,
                                avg_stack_price, avg_stack_frequency,
                                stack_cost)
            products.append(stack_product)

        return products
