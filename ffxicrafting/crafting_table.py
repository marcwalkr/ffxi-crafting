from controllers.synth_controller import SynthController
from synth import Synth


class CraftingTable:
    def __init__(self, crafter, sort_column, reverse_sort) -> None:
        self.crafter = crafter

        all_recipes = SynthController.get_all_recipes()
        synths = [Synth(r, crafter) for r in all_recipes]
        self.recipes = [s.recipe for s in synths if s.can_craft]

        self.sort_column = sort_column
        self.reverse_sort = reverse_sort
