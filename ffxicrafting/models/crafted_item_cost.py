class CraftedItemCost:
    def __init__(self, item_id, recipe_id, cost_per_unit, craft_skills, beastmen_controlled_regions, enabled_guilds,
                 auction_data_hash) -> None:
        self.item_id = item_id
        self.recipe_id = recipe_id
        self.cost_per_unit = cost_per_unit
        self.craft_skills = craft_skills
        self.beastmen_controlled_regions = beastmen_controlled_regions
        self.enabled_guilds = enabled_guilds
        self.auction_data_hash = auction_data_hash
