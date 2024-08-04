from __future__ import annotations
from typing import TYPE_CHECKING
from models import RecipeModel
from utils import unique_preserve_order

if TYPE_CHECKING:
    from entities import Ingredient, Result


class Recipe(RecipeModel):
    def __init__(self, id: int, desynth: bool, key_item: int, wood: int, smith: int, gold: int, cloth: int,
                 leather: int, bone: int, alchemy: int, cook: int, crystal: int, hq_crystal: int, ingredient1: int,
                 ingredient2: int, ingredient3: int, ingredient4: int, ingredient5: int, ingredient6: int,
                 ingredient7: int, ingredient8: int, result: int, result_hq1: int, result_hq2: int, result_hq3: int,
                 result_qty: int, result_hq1_qty: int, result_hq2_qty: int, result_hq3_qty: int, result_name: str,
                 ingredient_objects: list[Ingredient], result_objects: list[Result]) -> None:
        super().__init__(id, desynth, key_item, wood, smith, gold, cloth, leather, bone, alchemy, cook, crystal,
                         hq_crystal, ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6,
                         ingredient7, ingredient8, result, result_hq1, result_hq2, result_hq3, result_qty,
                         result_hq1_qty, result_hq2_qty, result_hq3_qty, result_name)

        # Populate ingredients dictionary
        self.ingredients: dict[Ingredient, int] = {}
        ingredient_ids = [crystal, ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6,
                          ingredient7, ingredient8]
        for item_id in ingredient_ids:
            if item_id > 0:
                ingredient = next((i for i in ingredient_objects if i.item_id == item_id), None)
                if ingredient:
                    self.ingredients[ingredient] = self.ingredients.get(ingredient, 0) + 1

        # Store results as a list of tuples (Result object, quantity, quality tier)
        self.results = []
        result_ids = [result, result_hq1, result_hq2, result_hq3]
        result_qtys = [result_qty, result_hq1_qty, result_hq2_qty, result_hq3_qty]
        quality_tiers = ["NQ", "HQ1", "HQ2", "HQ3"]
        for item_id, qty, tier in zip(result_ids, result_qtys, quality_tiers):
            result = next((r for r in result_objects if r.item_id == item_id), None)
            if result:
                self.results.append((result, qty, tier))

        self.cost: float | None = None

    def get_ingredients(self):
        return [ingredient for ingredient, count in self.ingredients.items() for _ in range(count)]

    def get_unique_ingredients(self):
        return list(self.ingredients.keys())

    def get_unique_results(self):
        seen = set()
        return [result for result, _, _ in self.results
                if not (result.item_id in seen or seen.add(result.item_id))]

    def get_nq_result(self):
        nq_result = next((r for r, q, t in self.results if t == "NQ"), None)
        if nq_result:
            qty = next(q for r, q, t in self.results if t == "NQ")
            return nq_result, qty
        return None, None

    def get_hq_result(self, hq_tier):
        hq_result = next((r for r, q, t in self.results if t == f"HQ{hq_tier}"), None)
        if hq_result:
            qty = next(q for r, q, t in self.results if t == f"HQ{hq_tier}")
            return hq_result, qty
        return None, None

    def get_formatted_ingredient_names(self):
        ingredient_strings = []
        for ingredient, count in self.ingredients.items():
            if count > 1:
                ingredient_strings.append(f"{ingredient.get_formatted_name()} x{count}")
            else:
                ingredient_strings.append(ingredient.get_formatted_name())
        return ", ".join(unique_preserve_order(ingredient_strings))

    def get_formatted_nq_result(self):
        nq_result = next((r for r, q, t in self.results if t == "NQ"), None)
        if nq_result:
            qty = next(q for r, q, t in self.results if t == "NQ")
            if qty > 1:
                return f"{nq_result.get_formatted_name()} x{qty}"
            else:
                return nq_result.get_formatted_name()
        return ""

    def get_formatted_hq_results(self):
        hq_strings = []
        for result, qty, tier in self.results:
            if tier.startswith("HQ"):
                hq_strings.append(f"{result.get_formatted_name()} x{qty}")
        return ", ".join(hq_strings)

    def get_formatted_levels_string(self):
        skills = {
            "Wood": self.wood,
            "Smith": self.smith,
            "Gold": self.gold,
            "Cloth": self.cloth,
            "Leather": self.leather,
            "Bone": self.bone,
            "Alchemy": self.alchemy,
            "Cook": self.cook
        }
        levels = [f"{skill} {level}" for skill, level in skills.items() if level > 0]
        return ", ".join(levels)

    def calculate_cost(self):
        cost = 0
        for ingredient, count in self.ingredients.items():
            min_cost = ingredient.get_min_cost()
            if min_cost is None:
                return None
            cost += min_cost * count
        self.cost = cost
        return cost
