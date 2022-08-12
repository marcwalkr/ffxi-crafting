from synth import Synth
from synth_row import SynthRow
from table import Table
from controllers.item_controller import ItemController


class SynthTable:
    def __init__(self, recipes, crafters, synth_trials, skill_look_ahead,
                 profit_threshold, frequency_threshold, sort_column,
                 reverse_sort) -> None:
        self.recipes = recipes
        self.crafters = crafters
        self.synth_trials = synth_trials
        self.skill_look_ahead = skill_look_ahead
        self.profit_threshold = profit_threshold
        self.frequency_threshold = frequency_threshold
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    def print(self):
        column_labels = ["Recipe ID", "NQ", "NQ Qty", "HQ1", "HQ1 Qty", "HQ2",
                         "HQ2 Qty", "HQ3", "HQ3 Qty", "Cost", "Avg Profit",
                         "Avg Sell Frequency"]

        synth_rows = []

        for recipe in self.recipes:
            synth = self.get_best_crafter(recipe)

            if synth is None:
                continue

            synth_cost = synth.calculate_cost()

            if synth_cost is None:
                continue

            hq1_item = ItemController.get_item(recipe.result_hq1)
            hq1_name = hq1_item.sort_name.replace("_", " ").title()

            hq2_item = ItemController.get_item(recipe.result_hq2)
            hq2_name = hq2_item.sort_name.replace("_", " ").title()

            hq3_item = ItemController.get_item(recipe.result_hq3)
            hq3_name = hq3_item.sort_name.replace("_", " ").title()

            averages = synth.calculate_averages(synth_cost, self.synth_trials)
            average_profit, average_sell_frequency = averages

            row = SynthRow(recipe.id, recipe.result_name, recipe.result_qty,
                           hq1_name, recipe.result_hq1_qty, hq2_name,
                           recipe.result_hq2_qty, hq3_name,
                           recipe.result_hq3_qty, synth_cost, average_profit,
                           average_sell_frequency)
            synth_rows.append(row)

        synth_rows = self.filter_rows(synth_rows)

        rows = [i.get() for i in synth_rows]

        table = Table(column_labels, rows, self.sort_column, self.reverse_sort)
        table.print()

    def get_best_crafter(self, recipe):
        best_crafter = Synth(recipe, self.crafters[0])
        for crafter in self.crafters:
            synth = Synth(recipe, crafter)
            skill_difference = synth.get_skill_difference()
            if skill_difference > best_crafter.get_skill_difference():
                best_crafter = synth

        enough_skill = (best_crafter.get_skill_difference() -
                        self.skill_look_ahead) >= 0

        has_key_item = True
        if recipe.key_item > 0:
            has_key_item = recipe.key_item in best_crafter.crafter.key_items

        if enough_skill and has_key_item:
            return best_crafter
        else:
            return None

    def filter_rows(self, synth_rows):
        profit_sorted = sorted(synth_rows, key=lambda i: i.average_profit,
                               reverse=True)
        filtered_rows = []
        for row in profit_sorted:
            duplicate = any(i.nq_name == row.nq_name and
                            i.hq1_name == row.hq1_name and
                            i.hq2_name == row.hq2_name and
                            i.hq3_name == row.hq3_name for i in filtered_rows)
            meets_profit = row.average_profit >= self.profit_threshold
            meets_frequency = row.average_frequency >= self.frequency_threshold

            if meets_profit and meets_frequency and not duplicate:
                filtered_rows.append(row)

        return filtered_rows
