from entities import Crafter
from config import SettingsManager


class CraftingController:
    def __init__(self, item_controller) -> None:
        self.item_controller = item_controller

    def simulate_craft(self, recipe):
        skills = SettingsManager.get_craft_skills()
        crafter = Crafter(*skills, recipe)
        results, profit_per_synth, profit_per_storage = crafter.craft(self.item_controller)

        if not results:
            return None

        sell_freq = max(
            max(result.single_sell_freq or 0, result.stack_sell_freq or 0)
            for result in results
        )

        return {
            "crafter": crafter,
            "profit_per_synth": profit_per_synth,
            "profit_per_storage": profit_per_storage,
            "sell_freq": sell_freq
        }
