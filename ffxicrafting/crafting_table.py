from operator import attrgetter
from synth import Synth
from product import Product
from table import Table
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

        rows = []

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

            if not self.meets_thresholds(synth):
                continue

            nq_name, hq1_name, hq2_name, hq3_name = synth.get_result_names()
            nq_qty, hq1_qty, hq2_qty, hq3_qty = synth.get_result_quantities()

            row = [synth.recipe.id, nq_name, nq_qty, hq1_name, hq1_qty,
                   hq2_name, hq2_qty, hq3_name, hq3_qty, synth.cost,
                   synth.profit, synth.sell_frequency]

            # A row already exists in the list with the same synth results
            duplicate = [r for r in rows if r[1] == row[1] and
                         r[3] == row[3] and r[5] == row[5] and r[7] == row[7]]

            if duplicate:
                duplicate_row = duplicate[0]

                # Take the row with the highest profit value
                row_profit = row[10]
                duplicate_profit = duplicate_row[10]

                if row_profit > duplicate_profit:
                    rows.remove(duplicate_row)
                    rows.append(row)
            else:
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
                products += self.create_products(synth, result_id)

        products += self.create_bundle_products(products)

        products = self.filter_thresholds(products)
        products = self.remove_product_duplicates(products)

        rows = []
        for product in products:
            row = [product.synth.recipe.id, product.name, product.quantity,
                   product.cost, product.sell_price, product.profit,
                   product.sell_frequency]

            rows.append(row)

        table = Table(column_labels, rows, self.sort_column, self.reverse_sort)
        table.print()

    def get_best_crafter(self, recipe):
        synths = [Synth(recipe, c) for c in self.crafters]
        can_craft = [s for s in synths if s.can_craft]

        if len(can_craft) == 0:
            return None

        # Synth object containing the crafter with the highest skill,
        # lowest synth "difficulty"
        best_crafter = min(can_craft, key=attrgetter("difficulty"))

        return best_crafter

    def meets_thresholds(self, obj):
        meets_profit = obj.profit >= self.profit_threshold
        meets_frequency = obj.sell_frequency >= self.frequency_threshold

        return meets_profit and meets_frequency

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
    def create_products(synth, item_id):
        item = ItemController.get_item(item_id)
        products = []

        single_product = Product(synth, item_id, 1)
        products.append(single_product)

        if item.stack_size > 1:
            stack_product = Product(synth, item_id, item.stack_size)
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

        wijnruit_price = 110
        carnation_price = 60

        products = []

        for product in all_products:
            if product.quantity != 99:
                continue

            item = ItemController.get_item(product.item_id)
            is_bundleable = any(i in item.name for i in bundleable_names)

            if not is_bundleable:
                continue

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

            if bundle is None:
                continue

            auction_stats = AuctionController.get_auction_stats(bundle.item_id)

            if auction_stats.no_sales:
                continue

            if "shuriken" in bundle.name or "toolbag" in bundle.name:
                single_bundled_cost = product.cost + wijnruit_price
            else:
                single_bundled_cost = product.cost + carnation_price

            if auction_stats.average_single_price is not None:
                single_price = auction_stats.average_single_price
                profit = single_price - single_bundled_cost
                single_freq = auction_stats.average_single_frequency
                single_product = Product(product.synth, bundle.item_id, 1,
                                         single_bundled_cost, single_price,
                                         profit, single_freq)
                products.append(single_product)

            if auction_stats.average_stack_price is not None:
                stack_bundled_cost = single_bundled_cost * bundle.stack_size
                stack_price = auction_stats.average_stack_price
                profit = stack_price - stack_bundled_cost
                stack_freq = auction_stats.average_stack_frequency
                stack_product = Product(product.synth, bundle.item_id,
                                        bundle.stack_size, stack_bundled_cost,
                                        stack_price, profit, stack_freq)
                products.append(stack_product)

        return products
