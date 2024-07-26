from models import CraftedCost
from config import SettingsManager
import json


class CraftedCostController:
    cache = {}

    def __init__(self, db) -> None:
        self.db = db
        self.beastmen_controlled_regions = json.dumps(SettingsManager.get_beastmen_controlled_regions())
        self.enabled_guilds = json.dumps(SettingsManager.get_enabled_guilds())

    def get_crafted_cost(self, item_id, recipe_id, crafter_tier):
        cache_key = (item_id, recipe_id, crafter_tier, self.beastmen_controlled_regions, self.enabled_guilds)
        if cache_key in self.cache:
            return self.cache[cache_key]
        else:
            crafted_cost_tuple = self.db.get_crafted_cost(item_id, recipe_id, crafter_tier,
                                                          self.beastmen_controlled_regions, self.enabled_guilds)
            if crafted_cost_tuple:
                crafted_cost = CraftedCost(*crafted_cost_tuple)
                self.cache[cache_key] = crafted_cost
            return crafted_cost

    def update_crafted_cost(self, item_id, recipe_id, crafter_tier, cost_per_unit, ingredient_costs):
        self.db.update_crafted_cost(item_id, recipe_id, crafter_tier, self.beastmen_controlled_regions,
                                    self.enabled_guilds, cost_per_unit, ingredient_costs)
        cache_key = (item_id, recipe_id, crafter_tier, self.beastmen_controlled_regions, self.enabled_guilds)
        self.cache[cache_key] = CraftedCost(item_id, recipe_id, cost_per_unit, crafter_tier,
                                            self.beastmen_controlled_regions, self.enabled_guilds, ingredient_costs)

    def store_crafted_cost(self, item_id, recipe_id, cost_per_unit, crafter_tier, ingredient_costs):
        self.db.store_crafted_cost(item_id, recipe_id, cost_per_unit, crafter_tier,
                                   self.beastmen_controlled_regions, self.enabled_guilds, ingredient_costs)
