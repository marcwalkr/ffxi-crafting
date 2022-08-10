from collections import defaultdict
from config import Config
from synth import Synth
from table import Table
from models.product import Product
from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from controllers.auction_controller import AuctionController


class ProductTable:
    def __init__(self, crafters, profit_threshold, frequency_threshold,
                 sort_column) -> None:
        self.crafters = crafters
        self.profit_threshold = profit_threshold
        self.frequency_threshold = frequency_threshold
        self.sort_column = sort_column

    def print(self):
        include_desynth = Config.get_include_desynth()
        recipes = SynthController.get_all_recipes()

        products = []

        for recipe in recipes:
            if recipe.desynth and not include_desynth:
                continue

            synth = self.get_best_crafter(recipe)

            # None of the crafters can make this recipe
            if synth is None:
                continue

            nq_item = ItemController.get_item(recipe.result)

            # Result item cannot be sold on AH
            if nq_item.ah == 0:
                continue

            synth_cost = synth.calculate_cost()

            if synth_cost is None:
                continue

            # Collect quantities in a dictionary to get expected quantity per
            # result item instead of separated by quality tier
            # key: result item id, value: expected quantity per synth
            expected_quantities = defaultdict(lambda: 0)
            expected_quantities[recipe.result] += synth.expected_nq_qty
            expected_quantities[recipe.result_hq1] += synth.expected_hq1_qty
            expected_quantities[recipe.result_hq2] += synth.expected_hq2_qty
            expected_quantities[recipe.result_hq3] += synth.expected_hq3_qty

            for result_id in expected_quantities:
                item = ItemController.get_item(result_id)

                expected_quantity = expected_quantities[result_id]
                single_cost = synth_cost / expected_quantity
                stack_cost = single_cost * item.stack_size

                products += self.create_products(recipe.id, result_id,
                                                 single_cost)

                bundleable_names = ["arrow", "bolt",
                                    "bullet", "shuriken", "card", "uchitake",
                                    "tsurara", "kawahori-ogi", "makibishi",
                                    "hiraishin", "mizu-deppo", "shihei",
                                    "jusatsu", "kaginawa", "sairui-ran",
                                    "kodoku", "shinobi-tabi",
                                    "sanjaku-tenugui", "soshi", "kabenro",
                                    "jinko", "ryuno", "mokujin",
                                    "inoshishinofuda", "shikanofuda",
                                    "chonofuda", "ranka", "furu"]
                if any(i in item.name for i in bundleable_names):
                    products += self.create_bundle_products(recipe.id,
                                                            item.name,
                                                            stack_cost)

        products = self.filter_products(products, self.profit_threshold,
                                        self.frequency_threshold)
        products = self.sort_products(products, self.sort_column)

        column_labels = ["Recipe ID", "Item Name", "Quantity",
                         "Cost", "Sell Price", "Profit", "Sell Frequency"]

        rows = []
        for product in products:
            rounded_cost = round(product.cost, 2)
            rounded_sell_price = round(product.sell_price, 2)
            rounded_profit = round(product.profit, 2)
            rounded_sell_frequency = round(product.sell_frequency, 2)

            row = [product.recipe_id, product.name, product.quantity,
                   rounded_cost, rounded_sell_price, rounded_profit,
                   rounded_sell_frequency]
            rows.append(row)

        table = Table(column_labels, rows)
        table.print()

    def get_best_crafter(self, recipe):
        skill_look_ahead = Config.get_skill_look_ahead()

        best_crafter = Synth(recipe, self.crafters[0])
        for crafter in self.crafters:
            synth = Synth(recipe, crafter)
            if synth.skill_difference < best_crafter.skill_difference:
                best_crafter = synth

        enough_skill = (best_crafter.skill_difference - skill_look_ahead) <= 0

        if recipe.key_item > 0:
            has_key_item = recipe.key_item in best_crafter.crafter.key_items
        else:
            has_key_item = True

        if enough_skill and has_key_item:
            return best_crafter
        else:
            return None

    @staticmethod
    def create_products(recipe_id, item_id, single_cost):
        item = ItemController.get_item(item_id)
        product_name = item.sort_name.replace("_", " ").title()

        auction_stats = AuctionController.get_auction_stats(item_id)

        avg_single_price = auction_stats.average_single_price
        avg_single_freq = auction_stats.average_single_frequency
        avg_stack_price = auction_stats.average_stack_price
        avg_stack_freq = auction_stats.average_stack_frequency

        products = []
        if avg_single_price is not None:
            single_product = Product(recipe_id, product_name, 1, single_cost,
                                     avg_single_price, avg_single_freq)
            products.append(single_product)

        if avg_stack_price is not None:
            stack_cost = single_cost * item.stack_size
            stack_product = Product(recipe_id, product_name, item.stack_size,
                                    stack_cost, avg_stack_price,
                                    avg_stack_freq)
            products.append(stack_product)

        return products

    @classmethod
    def create_bundle_products(cls, recipe_id, item_name, unbundled_cost):
        if item_name.endswith("arrow"):
            bundle_name = item_name.removesuffix("_arrow") + "_quiver"
        elif item_name.endswith("bolt"):
            bundle_name = item_name + "_quiver"
        elif item_name.endswith("bullet") or "shuriken" in item_name:
            bundle_name = item_name + "_pouch"
        elif item_name.endswith("card"):
            bundle_name = item_name + "_case"
        else:
            bundle_name = "toolbag_(" + item_name + ")"

        item = ItemController.get_item_by_name(bundle_name)

        if item is not None:
            # A wijnruit costs 120 gil, carnation costs 60 gil,
            if "shuriken" in item.name or "toolbag" in item.name:
                bundled_cost = unbundled_cost + 120
            else:
                bundled_cost = unbundled_cost + 60

            return cls.create_products(recipe_id, item.item_id, bundled_cost)
        else:
            return []

    @staticmethod
    def filter_products(products, profit_threshold, frequency_threshold):
        """Removes duplicates from different recipes that are less profitable
        and any that don't pass thresholds
        """
        profit_sorted = sorted(products, key=lambda x: x.profit, reverse=True)
        filtered = []
        for product in profit_sorted:
            duplicate = any(i.name == product.name and
                            i.quantity == product.quantity for i in filtered)
            profitable = product.profit >= profit_threshold
            fast_selling = product.sell_frequency >= frequency_threshold

            if profitable and fast_selling and not duplicate:
                filtered.append(product)

        return filtered

    @staticmethod
    def sort_products(products, sort_method):
        if sort_method == "name":
            sorted_products = sorted(products, key=lambda x: x.name)
        elif sort_method == "cost":
            sorted_products = sorted(products, key=lambda x: x.cost)
        elif sort_method == "profit":
            sorted_products = sorted(products, key=lambda x: x.profit,
                                     reverse=True)
        else:
            sorted_products = sorted(products, key=lambda x: x.sell_frequency,
                                     reverse=True)

        return sorted_products
