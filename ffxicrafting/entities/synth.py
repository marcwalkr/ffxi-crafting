from __future__ import annotations
from typing import TYPE_CHECKING
import random
from collections import defaultdict
from utils import clamp

if TYPE_CHECKING:
    from entities import Recipe, Crafter, Item


class Synth:
    """
    Represents a synthesis operation in the game, handling the crafting process
    and its outcomes based on crafter skills and recipe details.
    """
    _SUCCESS_PROBABILITY: float = 0.95
    _DESYNTH_SUCCESS_PROBABILITY: float = 0.45
    _MIN_SUCCESS_PROBABILITY: float = 0.05
    _MIN_HQ_PROBABILITY: float = 0.0006
    _HQ_PROBABILITIES: list[float] = [0.0006, 0.018, 0.0625, 0.25, 0.5]
    _DESYNTH_HQ_PROBABILITIES: list[float] = [0.37, 0.4, 0.43, 0.46, 0.49]
    _HQ_TIER_WEIGHTS: list[float] = [75, 18.75, 6.25]
    _DESYNTH_HQ_TIER_WEIGHTS: list[float] = [37.5, 37.5, 25]
    SIMULATION_TRIALS: int = 10000

    def __init__(self, recipe: Recipe, crafter: Crafter) -> None:
        """
        Initialize a Synth instance.

        Args:
            recipe (Recipe): The recipe to be synthesized.
            crafter (Crafter): The crafter performing the synthesis.
        """
        self._recipe: Recipe = recipe
        self._crafter: Crafter = crafter
        self._difficulty: int = self._get_difficulty()
        self.tier: int = self._get_tier()

    def _get_difficulty(self) -> int:
        """
        Calculate the difficulty of the synthesis based on recipe requirements and crafter skills.

        Returns:
            int: The calculated difficulty value.
        """
        recipe_skills = [
            (self._recipe.wood, self._crafter.wood),
            (self._recipe.smith, self._crafter.smith),
            (self._recipe.gold, self._crafter.gold),
            (self._recipe.cloth, self._crafter.cloth),
            (self._recipe.leather, self._crafter.leather),
            (self._recipe.bone, self._crafter.bone),
            (self._recipe.alchemy, self._crafter.alchemy),
            (self._recipe.cook, self._crafter.cook)
        ]

        max_required_skill = max((recipe for recipe, _ in recipe_skills if recipe > 0), default=0)
        if max_required_skill == 0:
            return 0

        corresponding_crafter_skill = next(crafter for recipe, crafter in recipe_skills if recipe == max_required_skill)

        return max_required_skill - corresponding_crafter_skill

    def _get_tier(self) -> int:
        """
        Determine the tier of the synthesis based on the difficulty.

        Returns:
            int: The synthesis tier (3, 2, 1, 0, or -1).
        """
        if self._difficulty < -50:
            return 3
        elif self._difficulty < -30:
            return 2
        elif self._difficulty < -10:
            return 1
        elif self._difficulty <= 0:
            return 0
        else:
            return -1

    def _attempt_success(self) -> bool:
        """
        Determine if the synthesis attempt is successful.

        Returns:
            bool: True if the synthesis is successful, False otherwise.
        """
        success_probability = self._SUCCESS_PROBABILITY - \
            (self._difficulty / 10) if self.tier == -1 else self._SUCCESS_PROBABILITY
        if self._recipe.desynth:
            success_probability = self._DESYNTH_SUCCESS_PROBABILITY - \
                (self._difficulty / 10) if self.tier == -1 else self._DESYNTH_SUCCESS_PROBABILITY
        return random.random() < max(success_probability, self._MIN_SUCCESS_PROBABILITY)

    def _attempt_hq(self) -> bool:
        """
        Determine if the synthesis results in a high-quality (HQ) item.

        Returns:
            bool: True if the synthesis produces an HQ item, False otherwise.
        """
        if self._recipe.desynth:
            hq_probability = self._DESYNTH_HQ_PROBABILITIES[self.tier + 1]
        else:
            hq_probability = self._HQ_PROBABILITIES[self.tier + 1]
        return random.random() < hq_probability

    def _get_hq_tier(self) -> int:
        """
        Determine the tier of the high-quality (HQ) result.

        Returns:
            int: The HQ tier (1, 2, or 3).
        """
        weights = self._DESYNTH_HQ_TIER_WEIGHTS if self._recipe.desynth else self._HQ_TIER_WEIGHTS
        return random.choices([1, 2, 3], weights=weights)[0]

    def _synth(self) -> tuple[Item, int]:
        """
        Perform a single synthesis attempt.

        Returns:
            tuple[Item, int]: A tuple containing the Item object and its quantity,
                                or (None, None) if the synthesis fails.
        """
        if self._attempt_success():
            if self._attempt_hq():
                hq_tier = self._get_hq_tier()
                return self._get_hq_result(hq_tier)
            return self._recipe.get_nq_result()
        return None, None

    def _get_hq_result(self, hq_tier: int) -> Item:
        """
        Get the high-quality (HQ) result for a given tier.

        Args:
            hq_tier (int): The HQ tier (1, 2, or 3).

        Returns:
            tuple[Item, int]: A tuple containing the HQ Item object and its quantity.
        """
        if hq_tier == 1:
            return self._recipe.get_hq_result(1)
        elif hq_tier == 2:
            return self._recipe.get_hq_result(2)
        else:
            return self._recipe.get_hq_result(3)

    def _do_synth_fail(self) -> dict[Item, int]:
        """
        Handle a failed synthesis attempt and determine retained ingredients.

        Returns:
            dict[Item, int]: A dictionary of retained ingredients and their quantities.
        """
        loss_probability = clamp(0.15 - (self._difficulty / 20), 0, 1) if self._difficulty > 0 else 0.15
        if self._recipe.desynth:
            loss_probability += 0.35

        ingredients = self._recipe.get_ingredients()[1:]  # Remove the crystal

        retained_ingredients = defaultdict(lambda: 0)
        for ingredient in ingredients:
            if random.random() >= loss_probability:
                retained_ingredients[ingredient] += 1

        return retained_ingredients

    def simulate(self) -> tuple[dict[Item, int], dict[Item, int]]:
        """
        Simulate multiple synthesis attempts and calculate the results.

        This method performs a specified number of synthesis attempts and tracks
        the results produced and ingredients retained from failed attempts.

        Returns:
            tuple[dict[Item, int], dict[Item, int]]: A tuple containing:
                - A dictionary of Items and their quantities produced during the simulation.
                - A dictionary of Items and their quantities retained from failed attempts.
        """
        results = defaultdict(lambda: 0)
        retained_ingredients = defaultdict(lambda: 0)

        for _ in range(self.SIMULATION_TRIALS):
            result, quantity = self._synth()
            if result is not None:
                results[result] += quantity
            else:
                retained = self._do_synth_fail()
                for result_retained, quantity_retained in retained.items():
                    retained_ingredients[result_retained] += quantity_retained

        return results, retained_ingredients
