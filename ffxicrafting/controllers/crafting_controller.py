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
            "results": results,
            "profit_per_synth": profit_per_synth,
            "profit_per_storage": profit_per_storage,
            "sell_freq": sell_freq
        }

    @staticmethod
    def format_search_table_row(craft_result):
        if not craft_result:
            return None

        crafter = craft_result["crafter"]
        recipe = crafter.recipe

        return {
            "nq_result": recipe.get_formatted_nq_result(),
            "hq_results": recipe.get_formatted_hq_results(),
            "levels": recipe.get_formatted_levels_string(),
            "ingredients": recipe.get_formatted_ingredient_names(),
            "synth_cost": int(crafter.synth.cost),
            "recipe_id": recipe.id
        }

    @staticmethod
    def format_profit_table_row(craft_result):
        if not craft_result:
            return None

        crafter = craft_result["crafter"]
        recipe = crafter.recipe

        return {
            "nq_result": recipe.get_formatted_nq_result(),
            "hq_results": recipe.get_formatted_hq_results(),
            "tier": crafter.synth.tier,
            "synth_cost": int(crafter.synth.cost),
            "profit_per_synth": int(craft_result["profit_per_synth"]),
            "profit_per_storage": int(craft_result["profit_per_storage"]),
            "sell_freq": float(f"{craft_result['sell_freq']}"),
            "recipe_id": recipe.id
        }
