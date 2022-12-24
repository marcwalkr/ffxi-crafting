from crafting_table import CraftingTable
from synth import Synth
from table import Table


class SynthTable(CraftingTable):
    def __init__(self, crafter, synth_profit_threshold,
                 inventory_profit_threshold, frequency_threshold, sort_column,
                 reverse_sort) -> None:
        super().__init__(crafter, frequency_threshold, sort_column,
                         reverse_sort)
        self.synth_profit_threshold = synth_profit_threshold
        self.inventory_profit_threshold = inventory_profit_threshold

    def print(self):
        column_labels = ["Recipe ID", "NQ", "NQ Qty", "HQ1", "HQ1 Qty", "HQ2",
                         "HQ2 Qty", "HQ3", "HQ3 Qty", "Cost",
                         "Profit Per Synth", "Profit Per Inventory",
                         "Sell Frequency"]

        rows = []

        for recipe in self.recipes:
            synth = Synth(recipe, self.crafter)

            synth.cost = synth.calculate_cost()

            # An ingredient price could not be found
            if synth.cost is None:
                continue

            synth.profit_per_synth, synth.profit_per_inventory, \
                synth.sell_frequency = synth.calculate_stats()

            meets_synth_profit = (synth.profit_per_synth >=
                                  self.synth_profit_threshold)
            meets_inventory_profit = (synth.profit_per_inventory >=
                                      self.inventory_profit_threshold)
            meets_frequency = synth.sell_frequency >= self.frequency_threshold

            if (not meets_synth_profit or not meets_inventory_profit or
                    not meets_frequency):
                continue

            nq_name, hq1_name, hq2_name, hq3_name = synth.get_result_names()
            nq_qty, hq1_qty, hq2_qty, hq3_qty = synth.get_result_quantities()

            row = [synth.recipe.id, nq_name, nq_qty, hq1_name, hq1_qty,
                   hq2_name, hq2_qty, hq3_name, hq3_qty, synth.cost,
                   synth.profit_per_synth, synth.profit_per_inventory,
                   synth.sell_frequency]

            # A row already exists in the list with the same synth results
            duplicate = [r for r in rows if r[1] == row[1] and
                         r[3] == row[3] and r[5] == row[5] and r[7] == row[7]]

            if duplicate:
                duplicate_row = duplicate[0]

                # Take the row with the highest profit per synth
                row_profit = row[10]
                duplicate_profit = duplicate_row[10]

                if row_profit > duplicate_profit:
                    rows.remove(duplicate_row)
                    rows.append(row)
            else:
                rows.append(row)

        table = Table(column_labels, rows, self.sort_column, self.reverse_sort)
        table.print()
