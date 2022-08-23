from operator import attrgetter
from synth import Synth
from controllers.synth_controller import SynthController


class CraftingTable:
    def __init__(self, crafters, frequency_threshold, sort_column,
                 reverse_sort) -> None:
        self.recipes = SynthController.get_all_recipes()
        self.crafters = crafters
        self.frequency_threshold = frequency_threshold
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort

    def get_best_crafter(self, recipe):
        synths = [Synth(recipe, c) for c in self.crafters]
        can_craft = [s for s in synths if s.can_craft]

        if len(can_craft) == 0:
            return None

        # Synth object containing the crafter with the highest skill,
        # lowest synth "difficulty"
        best_crafter = min(can_craft, key=attrgetter("difficulty"))

        return best_crafter
