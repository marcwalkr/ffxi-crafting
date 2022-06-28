import os
from pathlib import Path
from configparser import ConfigParser
from models.skill_set import SkillSet


class Config:
    path = Path(__file__)
    ROOT_DIR = path.parent.absolute()
    config_path = os.path.join(ROOT_DIR, "../config.ini")

    config = ConfigParser()
    config.read(config_path)

    def __init__(self) -> None:
        pass

    @classmethod
    def get_skill_set(cls, character_name):
        wood = cls.config.get(character_name, "wood")
        smith = cls.config.get(character_name, "smith")
        gold = cls.config.get(character_name, "gold")
        cloth = cls.config.get(character_name, "cloth")
        leather = cls.config.get(character_name, "leather")
        bone = cls.config.get(character_name, "bone")
        alchemy = cls.config.get(character_name, "alchemy")
        cook = cls.config.get(character_name, "cook")

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
    def get_key_items(cls, character_name):
        key_items = cls.config.get(character_name, "key_items")
        key_items = key_items.split(",")

        try:
            return [int(i) for i in key_items]
        except ValueError:
            return []

    @classmethod
    def get_thresholds(cls):
        profit = cls.config.get("thresholds", "profit")
        frequency = cls.config.get("thresholds", "frequency")
        value = cls.config.get("thresholds", "value")

        return int(profit), int(frequency), int(value)

    @classmethod
    def get_ignore_guilds(cls):
        return cls.config.getboolean("settings", "ignore_guilds")

    @classmethod
    def get_skill_range(cls):
        skill_range = cls.config.get("settings", "skill_range")
        return int(skill_range)

    @classmethod
    def get_monitored_item_ids(cls):
        item_ids = cls.config.get("auction_monitor", "item_ids")
        item_ids = item_ids.split(",")

        return [int(i) for i in item_ids]

    @classmethod
    def get_monitor_frequency(cls):
        frequency = cls.config.get("settings", "monitor_frequency")
        return int(frequency)

    @classmethod
    def get_include_desynth(cls):
        return cls.config.getboolean("settings", "include_desynth")
