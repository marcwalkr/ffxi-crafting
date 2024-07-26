class CraftedCost:
    def __init__(self, item_id, recipe_id, crafter_tier, beastmen_controlled_regions, enabled_guilds,
                 synth_cost, cost_per_unit) -> None:
        self.item_id = item_id
        self.recipe_id = recipe_id
        self.crafter_tier = crafter_tier
        self.beastmen_controlled_regions = beastmen_controlled_regions
        self.enabled_guilds = enabled_guilds
        self.synth_cost = synth_cost
        self.cost_per_unit = cost_per_unit
