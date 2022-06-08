class SkillSet:
    def __init__(self, wood, smith, gold, cloth, leather, bone, alchemy,
                 cook, *key_items) -> None:
        self.wood = wood
        self.smith = smith
        self.gold = gold
        self.cloth = cloth
        self.leather = leather
        self.bone = bone
        self.alchemy = alchemy
        self.cook = cook
        self.key_items = key_items
