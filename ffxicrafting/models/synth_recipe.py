class SynthRecipe:
    def __init__(self, id, desynth, key_item, wood, smith, gold, cloth,
                 leather, bone, alchemy, cook, crystal, hq_crystal,
                 ingredient1, ingredient2, ingredient3, ingredient4,
                 ingredient5, ingredient6, ingredient7, ingredient8, result,
                 result_hq1, result_hq2, result_hq3, result_qty,
                 result_hq1_qty, result_hq2_qty, result_hq3_qty,
                 result_name) -> None:
        self.id = id
        self.desynth = desynth
        self.key_item = key_item
        self.wood = wood
        self.smith = smith
        self.gold = gold
        self.cloth = cloth
        self.leather = leather
        self.bone = bone
        self.alchemy = alchemy
        self.cook = cook
        self.crystal = crystal
        self.hq_crystal = hq_crystal
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
        self.result_qty = result_qty
        self.result_hq1_qty = result_hq1_qty
        self.result_hq2_qty = result_hq2_qty
        self.result_hq3_qty = result_hq3_qty
        self.result_name = result_name
