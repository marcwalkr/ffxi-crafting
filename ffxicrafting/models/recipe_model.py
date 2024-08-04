class RecipeModel:
    """
    Represents a crafting recipe in the game.

    This class corresponds to a database table that stores information about crafting recipes,
    including required skills, ingredients, and possible results.
    """

    def __init__(self, id: int, desynth: bool, key_item: int, wood: int, smith: int, gold: int, cloth: int,
                 leather: int, bone: int, alchemy: int, cook: int, crystal: int, hq_crystal: int,
                 ingredient1: int, ingredient2: int, ingredient3: int, ingredient4: int, ingredient5: int,
                 ingredient6: int, ingredient7: int, ingredient8: int, result: int, result_hq1: int, result_hq2: int,
                 result_hq3: int, result_qty: int, result_hq1_qty: int, result_hq2_qty: int, result_hq3_qty: int,
                 result_name: str) -> None:
        """
        Initialize a RecipeModel instance.

        Args:
            id (int): The unique identifier for the recipe.
            desynth (bool): True if this is a desynthesis recipe, False otherwise.
            key_item (int): The item ID of the key item required for this recipe, if any.
            wood (int): The Woodworking skill level required for this recipe.
            smith (int): The Smithing skill level required for this recipe.
            gold (int): The Goldsmithing skill level required for this recipe.
            cloth (int): The Clothcraft skill level required for this recipe.
            leather (int): The Leathercraft skill level required for this recipe.
            bone (int): The Bonecraft skill level required for this recipe.
            alchemy (int): The Alchemy skill level required for this recipe.
            cook (int): The Cooking skill level required for this recipe.
            crystal (int): The item ID of the crystal required for this recipe.
            hq_crystal (int): The item ID of the HQ crystal for signing items.
            ingredient1 (int): The item ID of the first ingredient.
            ingredient2 (int): The item ID of the second ingredient.
            ingredient3 (int): The item ID of the third ingredient.
            ingredient4 (int): The item ID of the fourth ingredient.
            ingredient5 (int): The item ID of the fifth ingredient.
            ingredient6 (int): The item ID of the sixth ingredient.
            ingredient7 (int): The item ID of the seventh ingredient.
            ingredient8 (int): The item ID of the eighth ingredient.
            result (int): The item ID of the normal quality (NQ) result.
            result_hq1 (int): The item ID of the HQ1 (high quality tier 1) result.
            result_hq2 (int): The item ID of the HQ2 (high quality tier 2) result.
            result_hq3 (int): The item ID of the HQ3 (high quality tier 3) result.
            result_qty (int): The quantity of NQ items produced by this recipe.
            result_hq1_qty (int): The quantity of HQ1 items produced by this recipe.
            result_hq2_qty (int): The quantity of HQ2 items produced by this recipe.
            result_hq3_qty (int): The quantity of HQ3 items produced by this recipe.
            result_name (str): The name of the resulting item.

        Note:
            - Skill levels (wood, smith, etc.) of 0 indicate that the skill is not required for this recipe.
            - Ingredient item IDs of 0 indicate that the ingredient slot is not used in this recipe.
        """
        self.id: int = id
        self.desynth: bool = desynth
        self.key_item: int = key_item
        self.wood: int = wood
        self.smith: int = smith
        self.gold: int = gold
        self.cloth: int = cloth
        self.leather: int = leather
        self.bone: int = bone
        self.alchemy: int = alchemy
        self.cook: int = cook
        self.crystal: int = crystal
        self.hq_crystal: int = hq_crystal
        self.ingredient1: int = ingredient1
        self.ingredient2: int = ingredient2
        self.ingredient3: int = ingredient3
        self.ingredient4: int = ingredient4
        self.ingredient5: int = ingredient5
        self.ingredient6: int = ingredient6
        self.ingredient7: int = ingredient7
        self.ingredient8: int = ingredient8
        self.result: int = result
        self.result_hq1: int = result_hq1
        self.result_hq2: int = result_hq2
        self.result_hq3: int = result_hq3
        self.result_qty: int = result_qty
        self.result_hq1_qty: int = result_hq1_qty
        self.result_hq2_qty: int = result_hq2_qty
        self.result_hq3_qty: int = result_hq3_qty
        self.result_name: str = result_name
