from operator import attrgetter
from controllers.synth_controller import SynthController
from synth import Synth
from table import Table


class SynthTable:
    def __init__(self, crafters, synth_profit_threshold,
                 storage_profit_threshold, sort_column, reverse_sort) -> None:
        self.crafters = crafters

        all_recipes = SynthController.get_all_recipes()
        self.recipes = []

        for crafter in crafters:
            synths = [Synth(r, crafter) for r in all_recipes]
            self.recipes += [s.recipe for s in synths if s.can_craft and
                             s.recipe not in self.recipes]

        self.synth_profit_threshold = synth_profit_threshold
        self.storage_profit_threshold = storage_profit_threshold
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    def print(self):
        column_labels = ["Recipe ID", "NQ", "NQ Qty", "HQ1", "HQ1 Qty", "HQ2",
                         "HQ2 Qty", "HQ3", "HQ3 Qty", "Cost",
                         "Profit Per Synth", "Profit Per Storage"]

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

            synth.profit_per_synth, synth.profit_per_storage\
                = synth.calculate_stats()

            meets_synth_profit = (synth.profit_per_synth >=
                                  self.synth_profit_threshold)
            meets_inventory_profit = (synth.profit_per_storage >=
                                      self.storage_profit_threshold)

            if (not meets_synth_profit or not meets_inventory_profit):
                continue

            nq_name, hq1_name, hq2_name, hq3_name = synth.get_result_names()
            nq_qty, hq1_qty, hq2_qty, hq3_qty = synth.get_result_quantities()

            row = [synth.recipe.id, nq_name, nq_qty, hq1_name, hq1_qty,
                   hq2_name, hq2_qty, hq3_name, hq3_qty, synth.cost,
                   synth.profit_per_synth, synth.profit_per_storage]

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

    def get_best_crafter(self, recipe):
        synths = [Synth(recipe, c) for c in self.crafters]
        can_craft = [s for s in synths if s.can_craft]

        if len(can_craft) == 0:
            return None

        # Synth object containing the crafter with the highest skill,
        # lowest synth "difficulty"
        best_crafter = min(can_craft, key=attrgetter("difficulty"))

        return best_crafter
