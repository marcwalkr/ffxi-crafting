class CraftedCost:
    def __init__(self, item_id, recipe_id, cost_per_unit, crafter_tier, beastmen_controlled_regions, enabled_guilds,
                 ingredient_costs) -> None:
        self.item_id = item_id
        self.recipe_id = recipe_id
        self.cost_per_unit = cost_per_unit
        self.crafter_tier = crafter_tier
        self.beastmen_controlled_regions = beastmen_controlled_regions
        self.enabled_guilds = enabled_guilds
        self.ingredient_costs = ingredient_costs
