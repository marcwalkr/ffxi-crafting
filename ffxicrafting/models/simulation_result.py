class SimulationResult:
    def __init__(self, item_id, recipe_id, simulation_trials, crafter_tier, beastmen_regions, enabled_guilds,
                 synth_cost, simulation_cost, quantity, from_scratch, last_updated) -> None:
        self.item_id = item_id
        self.recipe_id = recipe_id
        self.simulation_trials = simulation_trials
        self.crafter_tier = crafter_tier
        self.beastmen_regions = beastmen_regions
        self.enabled_guilds = enabled_guilds
        self.synth_cost = synth_cost
        self.simulation_cost = simulation_cost
        self.quantity = quantity
        self.from_scratch = from_scratch
        self.last_updated = last_updated
