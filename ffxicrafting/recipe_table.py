from controllers.synth_controller import SynthController
from controllers.item_controller import ItemController
from synth import Synth
from table import Table


class RecipeTable:
    def __init__(self, crafter, craft_id, sort_column, reverse_sort) -> None:
        self.crafter = crafter
        self.craft_id = craft_id
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    def print(self):
        column_labels = ["Recipe ID", "Skill Cap", "NQ", "NQ Qty", "HQ1",
                         "HQ1 Qty", "HQ2", "HQ2 Qty", "HQ3", "HQ3 Qty"]
        rows = []

        all_recipes = SynthController.get_all_recipes()
        for recipe in all_recipes:
            synth = Synth(recipe, self.crafter)
            if synth.can_craft:
                skills = [recipe.wood, recipe.smith, recipe.gold, recipe.cloth,
                          recipe.leather, recipe.bone, recipe.alchemy,
                          recipe.cook]
                max_skill = max(skills)
                main_skill = skills.index(max_skill) + 1
                if main_skill == self.craft_id:
                    nq_item = ItemController.get_item(recipe.result)
                    hq1_item = ItemController.get_item(recipe.result_hq1)
                    hq2_item = ItemController.get_item(recipe.result_hq2)
                    hq3_item = ItemController.get_item(recipe.result_hq3)

                    nq_name = nq_item.sort_name.replace("_", " ").title()
                    hq1_name = hq1_item.sort_name.replace("_", " ").title()
                    hq2_name = hq2_item.sort_name.replace("_", " ").title()
                    hq3_name = hq3_item.sort_name.replace("_", " ").title()

                    nq_qty = recipe.result_qty
                    hq1_qty = recipe.result_hq1_qty
                    hq2_qty = recipe.result_hq2_qty
                    hq3_qty = recipe.result_hq3_qty

                    rows.append([recipe.id, max_skill, nq_name, nq_qty,
                                 hq1_name, hq1_qty, hq2_name, hq2_qty,
                                 hq3_name, hq3_qty])

        table = Table(column_labels, rows, self.sort_column, self.reverse_sort)
        table.print()
