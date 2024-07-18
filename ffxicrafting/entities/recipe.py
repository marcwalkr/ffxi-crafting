from models import RecipeModel
from utils import unique_preserve_order


class Recipe(RecipeModel):
    def __init__(self, id, desynth, key_item, wood, smith, gold, cloth, leather, bone, alchemy, cook, crystal_id,
                 hq_crystal, ingredient1_id, ingredient2_id, ingredient3_id, ingredient4_id, ingredient5_id,
                 ingredient6_id, ingredient7_id, ingredient8_id, result_id, result_hq1_id, result_hq2_id,
                 result_hq3_id, result_qty, result_hq1_qty, result_hq2_qty, result_hq3_qty, result_name, crystal,
                 ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, ingredient6, ingredient7,
                 ingredient8, result, result_hq1, result_hq2, result_hq3) -> None:
        super().__init__(id, desynth, key_item, wood, smith, gold, cloth, leather, bone, alchemy, cook, crystal_id,
                         hq_crystal, ingredient1_id, ingredient2_id, ingredient3_id, ingredient4_id, ingredient5_id,
                         ingredient6_id, ingredient7_id, ingredient8_id, result_id, result_hq1_id, result_hq2_id,
                         result_hq3_id, result_qty, result_hq1_qty, result_hq2_qty, result_hq3_qty, result_name)

        self.crystal = crystal
        self.ingredient1 = ingredient1
        self.ingredient2 = ingredient2
        self.ingredient3 = ingredient3
        self.ingredient4 = ingredient4
        self.ingredient5 = ingredient5
        self.ingredient6 = ingredient6
        self.ingredient7 = ingredient7
        self.ingredient8 = ingredient8
        self.result = result
        self.result_hq1 = result_hq1
        self.result_hq2 = result_hq2
        self.result_hq3 = result_hq3

    def get_formatted_ingredient_names(self):
        ingredients = self.get_ingredients()
        counts = self.get_ingredient_counts()
        return ", ".join([f"{ingredient.get_formatted_name()} x{counts[ingredient]}" for ingredient in ingredients])

    def get_formatted_nq_result(self):
        return self.result.get_formatted_name() + " x" + str(self.result_qty)

    def get_formatted_hq_results(self):
        hq_strings = [
            self.result_hq1.get_formatted_name() + " x" + str(self.result_hq1_qty),
            self.result_hq2.get_formatted_name() + " x" + str(self.result_hq2_qty),
            self.result_hq3.get_formatted_name() + " x" + str(self.result_hq3_qty)
        ]
        return ", ".join(unique_preserve_order(hq_strings))

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

    def get_results(self):
        return [self.result, self.result_hq1, self.result_hq2, self.result_hq3]

    def get_unique_results(self):
        return unique_preserve_order(self.get_results())

    def get_ingredients(self):
        ingredients = [
            self.crystal, self.ingredient1, self.ingredient2, self.ingredient3,
            self.ingredient4, self.ingredient5, self.ingredient6, self.ingredient7, self.ingredient8
        ]
        # Filter out None values
        return [ingredient for ingredient in ingredients if ingredient is not None]

    def get_unique_ingredients(self):
        return unique_preserve_order(self.get_ingredients())

    def get_ingredient_counts(self):
        ingredients = self.get_ingredients()
        ingredient_counts = {}
        for ingredient in ingredients:
            if ingredient in ingredient_counts:
                ingredient_counts[ingredient] += 1
            else:
                ingredient_counts[ingredient] = 1
        return ingredient_counts
