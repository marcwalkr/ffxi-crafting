import os
from pathlib import Path
from configparser import ConfigParser
from models.skill_set import SkillSet


class Config:
    path = Path(__file__)
    ROOT_DIR = path.parent.absolute()
    config_path = os.path.join(ROOT_DIR, "config.ini")

    config = ConfigParser()
    config.read(config_path)

    def __init__(self) -> None:
        pass

    @classmethod
    def get_skill_set(cls):
        wood = cls.config.get("skills", "wood")
        smith = cls.config.get("skills", "smith")
        gold = cls.config.get("skills", "gold")
        cloth = cls.config.get("skills", "cloth")
        leather = cls.config.get("skills", "leather")
        bone = cls.config.get("skills", "bone")
        alchemy = cls.config.get("skills", "alchemy")
        cook = cls.config.get("skills", "cook")

        skill_range = cls.get_skill_range()

        wood = int(wood) + skill_range
        smith = int(smith) + skill_range
        gold = int(gold) + skill_range
        cloth = int(cloth) + skill_range
        leather = int(leather) + skill_range
        bone = int(bone) + skill_range
        alchemy = int(alchemy) + skill_range
        cook = int(cook) + skill_range

        return SkillSet(wood, smith, gold, cloth, leather, bone, alchemy, cook)

    @classmethod
    def get_thresholds(cls):
        profit = cls.config.get("thresholds", "profit")
        frequency = cls.config.get("thresholds", "frequency")

        return int(profit), int(frequency)

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
