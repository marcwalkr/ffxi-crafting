from operator import attrgetter
from synth import Synth
from table import Table
from controllers.item_controller import ItemController


class SynthTable:
    def __init__(self, recipes, crafters, profit_threshold,
                 frequency_threshold, sort_column, reverse_sort) -> None:
        self.recipes = recipes
        self.crafters = crafters
        self.profit_threshold = profit_threshold
        self.frequency_threshold = frequency_threshold
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    def print(self):
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

            # An ingredient price couldn't be found
            if synth.cost is None:
                continue

            synth.profit, synth.sell_frequency = \
                synth.calculate_profit_and_frequency()

            synths.append(synth)

        synths = self.filter_synths(synths)

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

    def filter_synths(self, synths):
        profit_sorted = sorted(synths, key=lambda s: s.profit, reverse=True)

        filtered_synths = []
        for synth in profit_sorted:
            duplicate = any(s.recipe.result == synth.recipe.result and
                            s.recipe.result_hq1 == synth.recipe.result_hq1 and
                            s.recipe.result_hq2 == synth.recipe.result_hq2 and
                            s.recipe.result_hq3 == synth.recipe.result_hq3
                            for s in filtered_synths)
            meets_profit = synth.profit >= self.profit_threshold
            meets_frequency = synth.sell_frequency >= self.frequency_threshold

            if meets_profit and meets_frequency and not duplicate:
                filtered_synths.append(synth)

        return filtered_synths
