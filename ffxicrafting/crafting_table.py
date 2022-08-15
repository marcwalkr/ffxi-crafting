from operator import attrgetter
from synth import Synth
from product import Product
from table import Table
from ingredient import Ingredient
from controllers.item_controller import ItemController
from controllers.auction_controller import AuctionController


class CraftingTable:
    def __init__(self, recipes, crafters, profit_threshold,
                 frequency_threshold, sort_column, reverse_sort) -> None:
        self.recipes = recipes
        self.crafters = crafters
        self.profit_threshold = profit_threshold
        self.frequency_threshold = frequency_threshold
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    def print_synth_view(self):
        column_labels = ["Recipe ID", "NQ", "NQ Qty", "HQ1", "HQ1 Qty", "HQ2",
                         "HQ2 Qty", "HQ3", "HQ3 Qty", "Cost",
                         "Profit Per Synth", "Sell Frequency"]

        synths = []

        for recipe in self.recipes:
            synth = self.get_best_crafter(recipe)

            # None of the crafters can make this recipe
            if synth is None:
                continue

            synth.cost = synth.calculate_cost()

            # An ingredient price could not be found
            if synth.cost is None:
                continue

            synth.profit, synth.sell_frequency = \
                synth.calculate_profit_and_frequency()

            synths.append(synth)

        synths = self.filter_thresholds(synths)
        synths = self.remove_synth_duplicates(synths)

        rows = []
        for synth in synths:
            hq1_item = ItemController.get_item(synth.recipe.result_hq1)
            hq1_name = hq1_item.sort_name.replace("_", " ").title()

            hq2_item = ItemController.get_item(synth.recipe.result_hq2)
            hq2_name = hq2_item.sort_name.replace("_", " ").title()

            hq3_item = ItemController.get_item(synth.recipe.result_hq3)
            hq3_name = hq3_item.sort_name.replace("_", " ").title()

            row = [synth.recipe.id, synth.recipe.result_name,
                   synth.recipe.result_qty, hq1_name,
                   synth.recipe.result_hq1_qty, hq2_name,
                   synth.recipe.result_hq2_qty, hq3_name,
                   synth.recipe.result_hq3_qty, synth.cost,
                   synth.profit, synth.sell_frequency]

            rows.append(row)

        table = Table(column_labels, rows, self.sort_column, self.reverse_sort)
        table.print()

    def print_product_view(self):
        column_labels = ["Recipe ID", "Name", "Quantity", "Cost", "Sell Price",
                         "Profit", "Sell Frequency"]

        products = []

        for recipe in self.recipes:
            synth = self.get_best_crafter(recipe)

            # None of the crafters can make this recipe
            if synth is None:
                continue

            synth.cost = synth.calculate_cost()

            # An ingredient price could not be found
            if synth.cost is None:
                continue

            result_ids = [recipe.result, recipe.result_hq1, recipe.result_hq2,
                          recipe.result_hq3]

            # Remove duplicates
            result_ids = [*set(result_ids)]

            for result_id in result_ids:
                item = ItemController.get_item(result_id)
                stack_size = item.stack_size
                products += self.create_products(synth, result_id, stack_size)

        products += self.create_bundle_products(products)

        products = self.filter_thresholds(products)
        products = self.remove_product_duplicates(products)

        rows = []
        for product in products:
            item = ItemController.get_item(product.item_id)
            name = item.sort_name.replace("_", " ").title()

            row = [product.synth.recipe.id, name, product.quantity,
                   product.cost, product.sell_price, product.profit,
                   product.sell_frequency]

            rows.append(row)

        table = Table(column_labels, rows, self.sort_column, self.reverse_sort)
        table.print()

    def get_best_crafter(self, recipe):
        can_craft = []
        for crafter in self.crafters:
            synth = Synth(recipe, crafter)
            if synth.can_craft:
                can_craft.append(synth)

        if len(can_craft) == 0:
            return None

        best_crafter = min(can_craft, key=attrgetter("difficulty"))
        return best_crafter

    def remove_synth_duplicates(self, synths):
        profit_sorted = sorted(synths, key=lambda s: s.profit, reverse=True)

        removed_duplicates = []
        for synth in profit_sorted:
            duplicate = any(s.recipe.result == synth.recipe.result and
                            s.recipe.result_hq1 == synth.recipe.result_hq1 and
                            s.recipe.result_hq2 == synth.recipe.result_hq2 and
                            s.recipe.result_hq3 == synth.recipe.result_hq3
                            for s in removed_duplicates)

            if not duplicate:
                removed_duplicates.append(synth)

        return removed_duplicates

    def remove_product_duplicates(self, products):
        profit_sorted = sorted(products, key=lambda p: p.profit, reverse=True)

        removed_duplicates = []
        for product in profit_sorted:
            duplicate = any(p.item_id == product.item_id and
                            p.quantity == product.quantity
                            for p in removed_duplicates)

            if not duplicate:
                removed_duplicates.append(product)

        return removed_duplicates

    def filter_thresholds(self, object_list):
        filtered = []
        for obj in object_list:
            meets_profit = obj.profit >= self.profit_threshold
            meets_frequency = obj.sell_frequency >= self.frequency_threshold

            if meets_profit and meets_frequency:
                filtered.append(obj)

        return filtered

    @staticmethod
    def create_products(synth, item_id, stack_size):
        products = []

        single_product = Product(synth, item_id, 1)
        products.append(single_product)

        if stack_size > 1:
            stack_product = Product(synth, item_id, stack_size)
            products.append(stack_product)

        return products

    @staticmethod
    def create_bundle_products(all_products):
        bundleable_names = ["arrow", "bolt", "bullet", "shuriken", "card",
                            "uchitake", "tsurara", "kawahori-ogi", "makibishi",
                            "hiraishin", "mizu-deppo", "shihei", "jusatsu",
                            "kaginawa", "sairui-ran", "kodoku", "shinobi-tabi",
                            "sanjaku-tenugui", "soshi", "kabenro", "jinko",
                            "ryuno", "mokujin", "inoshishinofuda",
                            "shikanofuda", "chonofuda", "ranka", "furu"]

        wijnruit_item = ItemController.get_item_by_name("wijnruit")
        carnation_item = ItemController.get_item_by_name("carnation")

        wijnruit = Ingredient(wijnruit_item.item_id)
        carnation = Ingredient(carnation_item.item_id)

        products = []

        for product in all_products:
            item = ItemController.get_item(product.item_id)
            is_bundleable = any(i in item.name for i in bundleable_names)

            if product.quantity == 99 and is_bundleable:
                if item.name.endswith("arrow"):
                    bundle_name = item.name.removesuffix("_arrow") + "_quiver"
                elif item.name.endswith("bolt"):
                    bundle_name = item.name + "_quiver"
                elif item.name.endswith("bullet") or "shuriken" in item.name:
                    bundle_name = item.name + "_pouch"
                elif item.name.endswith("card"):
                    bundle_name = item.name + "_case"
                else:
                    bundle_name = "toolbag_(" + item.name + ")"

                bundle = ItemController.get_item_by_name(bundle_name)

                if bundle is not None:
                    stats = AuctionController.get_auction_stats(bundle.item_id)

                    if "shuriken" in bundle.name or "toolbag" in bundle.name:
                        single_bundled_cost = product.cost + wijnruit.price
                    else:
                        single_bundled_cost = product.cost + carnation.price

                    stack_bundled_cost = single_bundled_cost * bundle.stack_size

                    if stats.average_single_price is not None:
                        single_price = stats.average_single_price
                        profit = single_price - single_bundled_cost
                        single_freq = stats.average_single_frequency
                        single_product = Product(product.synth, bundle.item_id,
                                                 1, single_bundled_cost,
                                                 single_price, profit,
                                                 single_freq)
                        products.append(single_product)

                    if stats.average_stack_price is not None:
                        stack_price = stats.average_stack_price
                        profit = stack_price - stack_bundled_cost
                        stack_freq = stats.average_stack_frequency
                        stack_product = Product(product.synth, bundle.item_id,
                                                bundle.stack_size,
                                                stack_bundled_cost,
                                                stack_price, profit,
                                                stack_freq)
                        products.append(stack_product)

        return products
