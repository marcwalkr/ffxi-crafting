from crafting_table import CraftingTable
from product import Product
from table import Table
from synth import Synth
from controllers.item_controller import ItemController


class ProductTable(CraftingTable):
    def __init__(self, crafter, profit_threshold, frequency_threshold,
                 sort_column, reverse_sort) -> None:
        super().__init__(crafter, frequency_threshold, sort_column,
                         reverse_sort)
        self.profit_threshold = profit_threshold

    def print(self):
        column_labels = ["Recipe ID", "Name", "Quantity", "Cost", "Sell Price",
                         "Profit", "Sell Frequency"]

        products = []

        for recipe in self.recipes:
            synth = Synth(recipe, self.crafter)

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

        rows = []
        for product in products:
            row = [product.synth.recipe.id, product.name, product.quantity,
                   product.cost, product.sell_price, product.profit,
                   product.sell_frequency]

            # A row already exists in the list with the same name and quantity
            duplicate = [r for r in rows if r[1:3] == row[1:3]]

            if duplicate:
                duplicate_row = duplicate[0]

                # Take the row with the highest profit
                row_profit = row[5]
                duplicate_profit = duplicate_row[5]

                if row_profit > duplicate_profit:
                    rows.remove(duplicate_row)
                    rows.append(row)
            else:
                rows.append(row)

        table = Table(column_labels, rows, self.sort_column, self.reverse_sort)
        table.print()

    def create_products(self, synth, item_id):
        item = ItemController.get_item(item_id)
        products = []

        single_product = Product(synth, item_id, 1)
        products.append(single_product)

        if item.stack_size > 1:
            stack_product = Product(synth, item_id, item.stack_size)
            products.append(stack_product)
            if stack_product.can_bundle:
                products += stack_product.create_bundle_products()

        return [p for p in products if
                p.profit >= self.profit_threshold and
                p.sell_frequency >= self.frequency_threshold]
