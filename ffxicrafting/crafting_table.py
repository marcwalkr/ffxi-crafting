from operator import attrgetter
from controllers.synth_controller import SynthController
from synth import Synth


class CraftingTable:
    def __init__(self, crafters, sort_column,
                 reverse_sort, auction) -> None:
        self.crafters = crafters

        all_recipes = SynthController.get_all_recipes()
        self.recipes = []

        for crafter in crafters:
            synths = [Synth(r, crafter, auction) for r in all_recipes]
            self.recipes += [s.recipe for s in synths if s.can_craft and
                             s.recipe not in self.recipes]

        self.sort_column = sort_column
        self.reverse_sort = reverse_sort
        self.auction = auction

    def get_best_crafter(self, recipe):
        synths = [Synth(recipe, c, self.auction) for c in self.crafters]
        can_craft = [s for s in synths if s.can_craft]

        if len(can_craft) == 0:
            return None

        # Synth object containing the crafter with the highest skill,
        # lowest synth "difficulty"
        best_crafter = min(can_craft, key=attrgetter("difficulty"))

        return best_crafter
