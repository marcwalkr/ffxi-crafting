from controllers.synth_controller import SynthController


class CraftingTable:
    def __init__(self, crafter, frequency_threshold,
                 sort_column, reverse_sort) -> None:
        self.recipes = SynthController.get_all_recipes()
        self.crafter = crafter
        self.frequency_threshold = frequency_threshold
        self.sort_column = sort_column
        self.reverse_sort = reverse_sort
