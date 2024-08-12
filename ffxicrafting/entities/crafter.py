from __future__ import annotations
from typing import TYPE_CHECKING
from entities import Synth

if TYPE_CHECKING:
    from entities import Recipe, Item


class Crafter:
    """
    Represents a crafter in the game, capable of performing synthesis operations.
    """

    def __init__(self, wood: int, smith: int, gold: int, cloth: int, leather: int, bone: int, alchemy: int, cook: int,
                 recipe: Recipe) -> None:
        """
        Initialize a Crafter instance with crafting skills and a recipe.

        Args:
            wood (int): Woodworking crafting skill level.
            smith (int): Smithing crafting skill level.
            gold (int): Goldsmithing crafting skill level.
            cloth (int): Clothcraft crafting skill level.
            leather (int): Leatherworking crafting skill level.
            bone (int): Bonecraft crafting skill level.
            alchemy (int): Alchemy crafting skill level.
            cook (int): Cooking crafting skill level.
            recipe (Recipe): The recipe to be crafted.
        """
        self.wood: int = wood
        self.smith: int = smith
        self.gold: int = gold
        self.cloth: int = cloth
        self.leather: int = leather
        self.bone: int = bone
        self.alchemy: int = alchemy
        self.cook: int = cook
        self.recipe: Recipe = recipe
        self.synth: Synth = Synth(recipe, self)

    def craft(self) -> tuple[dict[Item, int], dict[Item, int]]:
        """
        Perform the crafting operation and calculate profits.

        Returns:
            tuple[dict[Item, int], dict[Item, int]]: A tuple containing the results of the crafting operation and the
            retained ingredients.

        Returns None if the recipe cannot be crafted due to missing ingredients.
        """
        if not self.recipe.min_cost:
            # The recipe cannot be crafted because of missing ingredients
            return None, None

        results, retained_ingredients = self.synth.simulate()
        return results, retained_ingredients
