from collections import OrderedDict
from entities import Item
from models import RecipeModel


class Recipe(RecipeModel):
    """
    Represents a crafting recipe in the game, extending the RecipeModel with additional
    functionality for managing ingredients and results.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Initialize a Recipe instance.

        Inherits all attributes from RecipeModel and initializes additional properties
        for managing ingredients and results.

        Args:
            *args: Variable length argument list for RecipeModel attributes.
            **kwargs: Arbitrary keyword arguments for RecipeModel attributes.
                Expects "ingredient_objects" and "result_objects" in kwargs.

        Attributes:
            ingredients (dict[Item, int]): A dictionary mapping ingredients to their quantities.
            results (OrderedDict[Item, list[tuple[int, str]]]): An ordered dictionary mapping Item objects 
                to a list of tuples containing their quantities and quality tiers.
            cost (float | None): The calculated cost of the recipe, if available.
        """
        super().__init__(*args)

        ingredient_objects = kwargs.get("ingredient_objects", [])
        result_objects = kwargs.get("result_objects", [])

        self.ingredients: dict[Item, int] = {}
        self._populate_ingredients(ingredient_objects)

        self._results: OrderedDict[Item, list[tuple[int, str]]] = OrderedDict()
        self._populate_results(result_objects)

        self.min_cost = self.calculate_cost()

    def _populate_ingredients(self, ingredient_objects: list[Item]) -> None:
        """
        Populate the ingredients dictionary from the provided ingredient objects.

        Args:
            ingredient_objects (list[Ingredient]): List of Ingredient objects to populate from.
        """
        ingredient_ids = [self.crystal, self.ingredient1, self.ingredient2, self.ingredient3,
                          self.ingredient4, self.ingredient5, self.ingredient6,
                          self.ingredient7, self.ingredient8]
        for item_id in ingredient_ids:
            if item_id > 0:
                ingredient = next((i for i in ingredient_objects if i.item_id == item_id), None)
                if ingredient:
                    self.ingredients[ingredient] = self.ingredients.get(ingredient, 0) + 1

    def _populate_results(self, result_objects: list[Item]) -> None:
        """
        Populate the results list from the provided result objects.

        Args:
            result_objects (list[Result]): List of Result objects to populate from.
        """
        result_ids = [self.result, self.result_hq1, self.result_hq2, self.result_hq3]
        result_qtys = [self.result_qty, self.result_hq1_qty, self.result_hq2_qty, self.result_hq3_qty]
        quality_tiers = ["NQ", "HQ1", "HQ2", "HQ3"]

        for item_id, qty, tier in zip(result_ids, result_qtys, quality_tiers):
            if item_id:
                result = next((r for r in result_objects if r.item_id == item_id), None)
                if result:
                    if result not in self._results:
                        self._results[result] = []
                    self._results[result].append((qty, tier))

    def get_ingredients(self) -> list[Item]:
        """
        Get a list of all ingredients, including duplicates.

        Returns:
            list[Ingredient]: A list of all ingredients, with each ingredient repeated
                              according to its quantity in the recipe.
        """
        return [ingredient for ingredient, count in self.ingredients.items() for _ in range(count)]

    def get_unique_ingredients(self) -> list[Item]:
        """
        Get a list of unique ingredients used in the recipe.

        Returns:
            list[Ingredient]: A list of unique ingredients.
        """
        return list(self.ingredients.keys())

    def get_unique_results(self) -> list[Item]:
        """
        Get a list of result objects representing the recipe's unique result items.

        Returns:
            list[Result]: A list of Result objects.
        """
        return list(self._results.keys())

    def get_nq_result(self) -> tuple[Item | None, int | None]:
        """
        Get the normal quality (NQ) result and its quantity.

        Returns:
            tuple[Result | None, int | None]: A tuple containing the NQ Result object and its quantity,
                                              or (None, None) if no NQ result exists.
        """
        for result, qty_tiers in self._results.items():
            for qty, tier in qty_tiers:
                if tier == "NQ":
                    return result, qty
        return None, None

    def get_hq_result(self, hq_tier: int) -> tuple[Item | None, int | None]:
        """
        Get the high quality (HQ) result of a specific tier and its quantity.

        Args:
            hq_tier (int): The HQ tier to retrieve (1, 2, or 3).

        Returns:
            tuple[Result | None, int | None]: A tuple containing the HQ Result object and its quantity,
                                              or (None, None) if no result exists for the specified tier.
        """
        for result, qty_tiers in self._results.items():
            for qty, tier in qty_tiers:
                if tier == f"HQ{hq_tier}":
                    return result, qty
        return None, None

    def get_formatted_ingredient_names(self) -> str:
        """
        Get a formatted string of ingredient names with their quantities.

        Returns:
            str: A comma-separated string of ingredient names with quantities.
        """
        ingredient_strings = []
        for ingredient, count in self.ingredients.items():
            if count > 1:
                ingredient_strings.append(f"{ingredient.get_formatted_name()} x{count}")
            else:
                ingredient_strings.append(ingredient.get_formatted_name())
        return ", ".join(ingredient_strings)

    def get_formatted_nq_result(self) -> str:
        """
        Get a formatted string representation of the normal quality (NQ) result.

        Returns:
            str: A string representing the NQ result with its quantity, or an empty string if no NQ result exists.
        """
        nq_result, qty = self.get_nq_result()
        if nq_result:
            if qty > 1:
                return f"{nq_result.get_formatted_name()} x{qty}"
            else:
                return nq_result.get_formatted_name()
        return ""

    def get_formatted_hq_results(self) -> str:
        """
        Get a formatted string representation of all high quality (HQ) results.

        Returns:
            str: A comma-separated string of HQ results with their quantities.
        """
        hq_strings = []
        for result, qty_tiers in self._results.items():
            for qty, tier in qty_tiers:
                if tier.startswith("HQ"):
                    hq_strings.append(f"{result.get_formatted_name()} x{qty}")
        return ", ".join(hq_strings)

    def get_formatted_levels_string(self) -> str:
        """
        Get a formatted string representation of the required crafting levels.

        Returns:
            str: A comma-separated string of crafting skills and their required levels.
        """
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

    def calculate_cost(self) -> float:
        """
        Calculate the min cost of the recipe based on the costs of its ingredients.

        Returns:
            float: The minimum cost of the recipe.
        """
        total_cost = 0
        for ingredient, count in self.ingredients.items():
            min_cost = ingredient.get_min_cost()
            if min_cost is None:
                return None
            total_cost += min_cost * count
        return total_cost
