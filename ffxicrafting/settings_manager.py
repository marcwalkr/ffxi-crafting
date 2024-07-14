import os
import json
from skill_set import SkillSet


class SettingsManager:
    SETTINGS_FILE = "settings.json"
    DEFAULT_SETTINGS = {
        "profit_table": {
            "profit_per_synth": 0,
            "profit_per_storage": 0,
            "min_sell_price": 0
        },
        "synth": {
            "skill_look_ahead": 0,
            "simulation_trials": 1000
        },
        "skill_levels": {
            "wood": 0,
            "smith": 0,
            "gold": 0,
            "cloth": 0,
            "leather": 0,
            "bone": 0,
            "alchemy": 0,
            "cook": 0
        },
        "merchants": {
            "guilds": True,
            "aragoneu": True,
            "derfland": True,
            "elshimo_lowlands": True,
            "elshimo_uplands": True,
            "fauregandi": True,
            "gustaberg": True,
            "kolshushu": True,
            "kuzotz": True,
            "li'telor": True,
            "movalpolos": True,
            "norvallen": True,
            "qufim": True,
            "ronfaure": True,
            "sarutabaruta": True,
            "tavnazian_archipelago": True,
            "valdeaunia": True,
            "vollbow": True,
            "zulkheim": True
        }
    }

    @classmethod
    def load_settings(cls):
        if os.path.exists(cls.SETTINGS_FILE):
            with open(cls.SETTINGS_FILE, "r") as file:
                return json.load(file)
        return cls.DEFAULT_SETTINGS

    @classmethod
    def save_settings(cls, settings):
        with open(cls.SETTINGS_FILE, "w") as file:
            json.dump(settings, file)

    @classmethod
    def get_enabled_merchants(cls):
        def format_merchant_name(name):
            if name == "li'telor":
                return "Li'Telor"
            return name.replace('_', ' ').title()

        settings = cls.load_settings()
        return [format_merchant_name(merchant) for merchant, enabled in settings["merchants"].items() if enabled]

    @classmethod
    def get_enabled_guilds(cls):
        settings = cls.load_settings()
        return settings["merchants"].get("guilds", False)

    @classmethod
    def get_skill_look_ahead(cls):
        settings = cls.load_settings()
        return settings["synth"].get("skill_look_ahead", 0)

    @classmethod
    def get_simulation_trials(cls):
        settings = cls.load_settings()
        return settings["synth"].get("simulation_trials", 1000)

    @classmethod
    def get_min_sell_price(cls):
        settings = cls.load_settings()
        return settings["profit_table"].get("min_sell_price", 0)

    @classmethod
    def get_skill_set(cls):
        settings = cls.load_settings()
        skills = settings.get("skills", {})
        return SkillSet(
            wood=skills.get("wood", 0),
            smith=skills.get("smith", 0),
            gold=skills.get("gold", 0),
            cloth=skills.get("cloth", 0),
            leather=skills.get("leather", 0),
            bone=skills.get("bone", 0),
            alchemy=skills.get("alchemy", 0),
            cook=skills.get("cook", 0)
        )
