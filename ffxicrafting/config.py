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

    @classmethod
    def get_synth_profit_threshold(cls):
        profit = cls.config.get("thresholds", "synth_profit")
        return int(profit)

    @classmethod
    def get_synth_frequency_threshold(cls):
        frequency = cls.config.get("thresholds", "synth_frequency")
        return float(frequency)

    @classmethod
    def get_product_profit_threshold(cls):
        profit = cls.config.get("thresholds", "product_profit")
        return int(profit)

    @classmethod
    def get_product_frequency_threshold(cls):
        frequency = cls.config.get("thresholds", "product_frequency")
        return float(frequency)

    @classmethod
    def get_ignore_guilds(cls):
        return cls.config.getboolean("settings", "ignore_guilds")

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
    def get_product_sort_column(cls):
        return cls.config.get("settings", "product_sort_column")

    @classmethod
    def get_reverse_sort(cls):
        return cls.config.getboolean("settings", "reverse_sort")

    @classmethod
    def get_monitored_item_ids(cls):
        item_ids = cls.config.get("auction_monitor", "item_ids")
        item_ids = item_ids.split(",")

        return [int(i) for i in item_ids]
