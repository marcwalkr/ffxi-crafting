import os
from dotenv import load_dotenv
from skill_set import SkillSet


class Config:
    load_dotenv(".env")  # Load environment variables from .env file

    @classmethod
    def get_profit_per_synth(cls):
        return int(os.getenv("PROFIT_PER_SYNTH"))

    @classmethod
    def get_profit_per_storage(cls):
        return int(os.getenv("PROFIT_PER_STORAGE"))

    @classmethod
    def get_store_item(cls):
        return int(os.getenv("STORE_ITEM"))

    @classmethod
    def get_ignore_guilds(cls):
        return os.getenv("IGNORE_GUILDS").lower() == "true"

    @classmethod
    def get_ignored_regions(cls):
        regions = [
            "Aragoneu", "Derfland", "Elshimo Lowlands", "Elshimo Uplands",
            "Fauregandi", "Gustaberg", "Kolshushu", "Kuzotz", "Li'Telor",
            "Movalpolos", "Norvallen", "Qufim", "Ronfaure", "Sarutabaruta",
            "Tavnazian Archipelago", "Valdeaunia", "Vollbow", "Zulkheim"
        ]
        ignored_regions = []

        for region in regions:
            env_var_name = f"IGNORE_{region.upper().replace(" ", "_").replace("'", "_")}"
            if os.getenv(env_var_name).lower() == "true":
                ignored_regions.append(region)

        return ignored_regions

    @classmethod
    def get_spreadsheet_id(cls):
        return os.getenv("SPREADSHEET_ID")

    @classmethod
    def get_skill_look_ahead(cls):
        return int(os.getenv("SKILL_LOOK_AHEAD"))

    @classmethod
    def get_simulation_trials(cls):
        return int(os.getenv("SIMULATION_TRIALS"))

    @classmethod
    def get_synth_sort_column(cls):
        return os.getenv("SYNTH_SORT_COLUMN")

    @classmethod
    def get_reverse_sort(cls):
        return os.getenv("REVERSE_SORT").lower() == "true"

    @classmethod
    def get_skill_set(cls):
        wood = int(os.getenv("WOOD"))
        smith = int(os.getenv("SMITH"))
        gold = int(os.getenv("GOLD"))
        cloth = int(os.getenv("CLOTH"))
        leather = int(os.getenv("LEATHER"))
        bone = int(os.getenv("BONE"))
        alchemy = int(os.getenv("ALCHEMY"))
        cook = int(os.getenv("COOK"))

        return SkillSet(wood, smith, gold, cloth, leather, bone, alchemy, cook)
