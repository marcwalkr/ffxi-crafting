import os
import json


class SettingsManager:
    SETTINGS_FILE = "settings.json"
    DEFAULT_SETTINGS = {
        "profit_table": {
            "profit_/_synth": 0,
            "profit_/_storage": 0,
            "min_sell_price": 0,
            "sell_frequency": 0.0,
            "craft_ingredients": False
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
        "regional_merchants": {
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
        },
        "guilds": {
            "alchemy": True,
            "bonecraft": True,
            "clothcraft": True,
            "cooking": True,
            "fishing": True,
            "goldsmithing": True,
            "leathercraft": True,
            "smithing": True,
            "woodworking": True,
            "tenshodo": True
        },
        "database": {
            "host": "",
            "user": "",
            "password": "",
            "database": ""
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
            json.dump(settings, file, indent=4)

    @classmethod
    def get_profit_per_synth(cls):
        settings = cls.load_settings()
        return settings["profit_table"].get("profit_/_synth", 0)

    @classmethod
    def get_profit_per_storage(cls):
        settings = cls.load_settings()
        return settings["profit_table"].get("profit_/_storage", 0)

    @classmethod
    def get_min_sell_price(cls):
        settings = cls.load_settings()
        return settings["profit_table"].get("min_sell_price", 0)

    @classmethod
    def get_sell_freq(cls):
        settings = cls.load_settings()
        return settings["profit_table"].get("sell_frequency", 0.0)

    @classmethod
    def get_craft_ingredients(cls):
        settings = cls.load_settings()
        return settings["profit_table"].get("craft_ingredients", False)

    @classmethod
    def get_skill_look_ahead(cls):
        settings = cls.load_settings()
        return settings["synth"].get("skill_look_ahead", 0)

    @classmethod
    def get_simulation_trials(cls):
        settings = cls.load_settings()
        return settings["synth"].get("simulation_trials", 1000)

    @classmethod
    def get_skills(cls):
        settings = cls.load_settings()
        skills = settings.get("skill_levels", {})
        return [
            skills.get("wood", 0),
            skills.get("smith", 0),
            skills.get("gold", 0),
            skills.get("cloth", 0),
            skills.get("leather", 0),
            skills.get("bone", 0),
            skills.get("alchemy", 0),
            skills.get("cook", 0)
        ]

    @classmethod
    def get_enabled_regional_merchants(cls):
        def format_merchant_name(name):
            if name == "li'telor":
                return "Li'Telor"
            return name.replace('_', ' ').title()

        settings = cls.load_settings()
        merchants = settings["regional_merchants"].items()
        enabled_merchants = [merchant for merchant, enabled in merchants if enabled]
        return [format_merchant_name(merchant) for merchant in enabled_merchants]

    @classmethod
    def get_enabled_guilds(cls):
        settings = cls.load_settings()
        guilds = settings["guilds"].items()
        enabled_guilds = [guild for guild, enabled in guilds if enabled]
        return [guild.capitalize() for guild in enabled_guilds]

    @classmethod
    def get_database_host(cls):
        settings = cls.load_settings()
        return settings["database"].get("host", "")

    @classmethod
    def get_database_user(cls):
        settings = cls.load_settings()
        return settings["database"].get("user", "")

    @classmethod
    def get_database_password(cls):
        settings = cls.load_settings()
        return settings["database"].get("password", "")

    @classmethod
    def get_database_name(cls):
        settings = cls.load_settings()
        return settings["database"].get("database", "")
