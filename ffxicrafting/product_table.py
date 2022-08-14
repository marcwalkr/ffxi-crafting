from operator import attrgetter
from synth import Synth
from product import Product
from table import Table
from controllers.item_controller import ItemController


class ProductTable:
    def __init__(self, recipes, crafters, profit_threshold,
                 frequency_threshold, sort_column, reverse_sort) -> None:
        self.recipes = recipes
        self.crafters = crafters
        self.profit_threshold = profit_threshold
        self.frequency_threshold = frequency_threshold
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    def print(self):
        column_labels = ["Recipe ID", "Name", "Quantity", "Cost", "Sell Price",
                         "Profit", "Sell Frequency"]

        products = []

        for recipe in self.recipes:
            synth = self.get_best_crafter(recipe)

            # None of the crafters can make this recipe
            if synth is None:
                continue

            result_ids = [recipe.result, recipe.result_hq1, recipe.result_hq2,
                          recipe.result_hq3]

            # Remove duplicates
            result_ids = [*set(result_ids)]

            for result_id in result_ids:
                item = ItemController.get_item(result_id)
                single_product = Product(recipe, synth.crafter, result_id, 1)
                if (single_product.cost is not None and
                    single_product.sell_price is not None and
                    single_product.profit is not None and
                        single_product.sell_frequency is not None):
                    products.append(single_product)

                if item.stack_size > 1:
                    stack_product = Product(recipe, synth.crafter, result_id,
                                            item.stack_size)
                    if (stack_product.cost is not None and
                        stack_product.sell_price is not None and
                        stack_product.profit is not None and
                            stack_product.sell_frequency is not None):
                        products.append(stack_product)

        products = self.filter_products(products)

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

    def filter_products(self, products):
        profit_sorted = sorted(products, key=lambda s: s.profit, reverse=True)

        filtered_products = []
        for product in profit_sorted:
            duplicate = any(p.item_id == product.item_id and
                            p.quantity == product.quantity
                            for p in filtered_products)
            meets_profit = product.profit >= self.profit_threshold
            meets_frequency = (product.sell_frequency >=
                               self.frequency_threshold)

            if meets_profit and meets_frequency and not duplicate:
                filtered_products.append(product)

        return filtered_products
