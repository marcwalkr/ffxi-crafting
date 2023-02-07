import os
from pathlib import Path
from configparser import ConfigParser
from skill_set import SkillSet


class Config:
    path = Path(__file__)
    ROOT_DIR = path.parent.absolute()
    config_path = os.path.join(ROOT_DIR, "../config.ini")

    config = ConfigParser()
    config.read(config_path)

    def __init__(self) -> None:
        pass

    @classmethod
    def get_profit_per_synth(cls):
        profit = cls.config.get("thresholds", "profit_per_synth")
        return int(profit)

    @classmethod
    def get_profit_per_storage(cls):
        profit = cls.config.get("thresholds", "profit_per_storage")
        return int(profit)

    @classmethod
    def get_store_item(cls):
        store_item = cls.config.get("thresholds", "store_item")
        return int(store_item)

    @classmethod
    def get_ignore_guilds(cls):
        return cls.config.getboolean("settings", "ignore_guilds")

    @classmethod
    def get_ignored_regions(cls):
        ignored_regions = []

        if cls.config.getboolean("settings", "ignore_aragoneu"):
            ignored_regions.append("Aragoneu")

        if cls.config.getboolean("settings", "ignore_derfland"):
            ignored_regions.append("Derfland")

        if cls.config.getboolean("settings", "ignore_elshimo_lowlands"):
            ignored_regions.append("Elshimo Lowlands")

        if cls.config.getboolean("settings", "ignore_elshimo_uplands"):
            ignored_regions.append("Elshimo Uplands")

        if cls.config.getboolean("settings", "ignore_fauregandi"):
            ignored_regions.append("Fauregandi")

        if cls.config.getboolean("settings", "ignore_gustaberg"):
            ignored_regions.append("Gustaberg")

        if cls.config.getboolean("settings", "ignore_kolshushu"):
            ignored_regions.append("Kolshushu")

        if cls.config.getboolean("settings", "ignore_kuzotz"):
            ignored_regions.append("Kuzotz")

        if cls.config.getboolean("settings", "ignore_li_telor"):
            ignored_regions.append("Li'Telor")

        if cls.config.getboolean("settings", "ignore_movalpolos"):
            ignored_regions.append("Movalpolos")

        if cls.config.getboolean("settings", "ignore_norvallen"):
            ignored_regions.append("Norvallen")

        if cls.config.getboolean("settings", "ignore_qufim"):
            ignored_regions.append("Qufim")

        if cls.config.getboolean("settings", "ignore_ronfaure"):
            ignored_regions.append("Ronfaure")

        if cls.config.getboolean("settings", "ignore_sarutabaruta"):
            ignored_regions.append("Sarutabaruta")

        if cls.config.getboolean("settings", "ignore_tavnazian_archipelago"):
            ignored_regions.append("Tavnazian Archipelago")

        if cls.config.getboolean("settings", "ignore_valdeaunia"):
            ignored_regions.append("Valeaunia")

        if cls.config.getboolean("settings", "ignore_vollbow"):
            ignored_regions.append("Vollbow")

        if cls.config.getboolean("settings", "ignore_zulkheim"):
            ignored_regions.append("Zulkheim")

        return ignored_regions

    @classmethod
    def get_spreadsheet_id(cls):
        return cls.config.get("secrets", "spreadsheet_id")

    @classmethod
    def get_skill_look_ahead(cls):
        skill_look_ahead = cls.config.get("settings", "skill_look_ahead")
        return int(skill_look_ahead)

    @classmethod
    def get_simulation_trials(cls):
        trials = cls.config.get("settings", "simulation_trials")
        return int(trials)

    @classmethod
    def get_synth_sort_column(cls):
        return cls.config.get("settings", "synth_sort_column")

    @classmethod
    def get_reverse_sort(cls):
        return cls.config.getboolean("settings", "reverse_sort")

    @classmethod
    def get_skill_set(cls, character):
        wood = cls.config.get(character, "wood")
        smith = cls.config.get(character, "smith")
        gold = cls.config.get(character, "gold")
        cloth = cls.config.get(character, "cloth")
        leather = cls.config.get(character, "leather")
        bone = cls.config.get(character, "bone")
        alchemy = cls.config.get(character, "alchemy")
        cook = cls.config.get(character, "cook")

        wood = int(wood)
        smith = int(smith)
        gold = int(gold)
        cloth = int(cloth)
        leather = int(leather)
        bone = int(bone)
        alchemy = int(alchemy)
        cook = int(cook)

        return SkillSet(wood, smith, gold, cloth, leather, bone, alchemy, cook)

    @classmethod
    def get_key_items(cls, character):
        key_items = cls.config.get(character, "key_items")
        key_items = key_items.split(",")

        try:
            return [int(i) for i in key_items]
        except ValueError:
            return []
