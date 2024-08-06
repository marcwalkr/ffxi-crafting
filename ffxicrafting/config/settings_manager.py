import os
import json


class SettingsManager:
    """
    A class for managing application settings.

    This class provides methods to load, save, and retrieve various settings
    used throughout the FFXI Crafting Tool application. It handles the persistence
    of settings to a JSON file and provides default values when settings are not found.
    """

    SETTINGS_FILE = "settings.json"
    DEFAULT_SETTINGS = {
        "thresholds_and_settings": {
            "profit_/_synth": 0,
            "profit_/_storage": 0,
            "min_auction_list_price": 0,
            "sell_frequency": 0.0,
            "craft_ingredients": False
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
            "aragoneu": "San d'Oria",
            "derfland": "San d'Oria",
            "elshimo_lowlands": "San d'Oria",
            "elshimo_uplands": "San d'Oria",
            "fauregandi": "San d'Oria",
            "gustaberg": "San d'Oria",
            "kolshushu": "San d'Oria",
            "kuzotz": "San d'Oria",
            "li'telor": "San d'Oria",
            "movalpolos": "San d'Oria",
            "norvallen": "San d'Oria",
            "qufim": "San d'Oria",
            "ronfaure": "San d'Oria",
            "sarutabaruta": "San d'Oria",
            "tavnazian_archipelago": "San d'Oria",
            "valdeaunia": "San d'Oria",
            "vollbow": "San d'Oria",
            "zulkheim": "San d'Oria"
        },
        "conquest": {
            "sandoria": "1st",
            "bastok": "2nd",
            "windurst": "3rd"
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
    def load_settings(cls) -> dict:
        """
        Load settings from the settings file.

        Returns:
            dict: A dictionary containing the loaded settings. If the settings file
            doesn't exist, returns the default settings.
        """
        if os.path.exists(cls.SETTINGS_FILE):
            with open(cls.SETTINGS_FILE, "r") as file:
                return json.load(file)
        return cls.DEFAULT_SETTINGS

    @classmethod
    def save_settings(cls, settings: dict) -> None:
        """
        Save settings to the settings file.

        Args:
            settings (dict): A dictionary containing the settings to be saved.
        """
        with open(cls.SETTINGS_FILE, "w") as file:
            json.dump(settings, file, indent=4)

    @classmethod
    def get_profit_per_synth(cls) -> int:
        """
        Get the profit per synthesis setting.

        Returns:
            int: The profit per synthesis value. Returns 0 if not set.
        """
        settings = cls.load_settings()
        return settings["thresholds_and_settings"].get("profit_/_synth", 0)

    @classmethod
    def get_profit_per_storage(cls) -> int:
        """
        Get the profit per storage setting.

        Returns:
            int: The profit per storage value. Returns 0 if not set.
        """
        settings = cls.load_settings()
        return settings["thresholds_and_settings"].get("profit_/_storage", 0)

    @classmethod
    def get_sell_freq(cls) -> float:
        """
        Get the sell frequency setting.

        Returns:
            float: The sell frequency value. Returns 0.0 if not set.
        """
        settings = cls.load_settings()
        return settings["thresholds_and_settings"].get("sell_frequency", 0.0)

    @classmethod
    def get_craft_ingredients(cls) -> bool:
        """
        Get the craft ingredients setting.

        Returns:
            bool: True if craft ingredients is enabled, False otherwise.
        """
        settings = cls.load_settings()
        return settings["thresholds_and_settings"].get("craft_ingredients", False)

    @classmethod
    def get_craft_skills(cls) -> list[int]:
        """
        Get the craft skills settings.

        Returns:
            list[int]: A list of craft skill levels for each crafting discipline.
            Returns [0, 0, 0, 0, 0, 0, 0, 0] if not set.
        """
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
    def get_regional_merchants(cls) -> dict:
        """
        Get the regional merchants settings.

        Returns:
            dict: A dictionary of regions and their controlling nations.
            Returns the default settings if not set.
        """
        settings = cls.load_settings()
        return settings.get("regional_merchants", cls.DEFAULT_SETTINGS["regional_merchants"])

    @classmethod
    def get_beastmen_regions(cls) -> list[str]:
        """
        Get the list of regions controlled by beastmen.

        Returns:
            list[str]: A list of region names controlled by beastmen.
        """
        settings = cls.load_settings()
        regions = []
        regional_merchants = settings.get("regional_merchants", cls.DEFAULT_SETTINGS["regional_merchants"])
        for region, control in regional_merchants.items():
            if control == "Beastmen":
                region_name = region.replace("_", " ")
                regions.append(region_name)
        return regions

    @classmethod
    def get_conquest_ranking(cls) -> dict[str, str]:
        """
        Get the conquest ranking.

        Returns:
            dict[str, str]: A dictionary of the nations and their conquest rankings.
        """
        return cls.load_settings().get("conquest", cls.DEFAULT_SETTINGS["conquest"])

    @classmethod
    def get_sandoria_rank(cls) -> int:
        """
        Get the conquest rank for San d'Oria.

        Returns:
            int: The conquest rank for San d'Oria (1-3). Returns 3 if not set or invalid.
        """
        return cls._rank_str_to_int(cls.get_conquest_ranking().get("san doria", "3rd"))

    @classmethod
    def get_bastok_rank(cls) -> int:
        """
        Get the conquest rank for Bastok.

        Returns:
            int: The conquest rank for Bastok (1-3). Returns 3 if not set or invalid.
        """
        return cls._rank_str_to_int(cls.get_conquest_ranking().get("bastok", "3rd"))

    @classmethod
    def get_windurst_rank(cls) -> int:
        """
        Get the conquest rank for Windurst.

        Returns:
            int: The conquest rank for Windurst (1-3). Returns 3 if not set or invalid.
        """
        return cls._rank_str_to_int(cls.get_conquest_ranking().get("windurst", "3rd"))

    @staticmethod
    def _rank_str_to_int(rank_str: str) -> int:
        """
        Convert a rank string to its corresponding integer value.

        Args:
            rank_str (str): The rank as a string ("1st", "2nd", or "3rd").

        Returns:
            int: The rank as an integer (1, 2, or 3). Returns 1 if invalid.
        """
        rank_map = {"1st": 1, "2nd": 2, "3rd": 3}
        return rank_map.get(rank_str, 1)

    @classmethod
    def get_enabled_guilds(cls) -> list[str]:
        """
        Get the list of enabled guilds.

        Returns:
            list[str]: A list of enabled guild names, capitalized.
        """
        settings = cls.load_settings()
        guilds = settings["guilds"].items()
        enabled_guilds = [guild for guild, enabled in guilds if enabled]
        return [guild.capitalize() for guild in enabled_guilds]

    @classmethod
    def get_database_host(cls) -> str:
        """
        Get the database host setting.

        Returns:
            str: The database host. Returns an empty string if not set.
        """
        settings = cls.load_settings()
        return settings["database"].get("host", "")

    @classmethod
    def get_database_user(cls) -> str:
        """
        Get the database user setting.

        Returns:
            str: The database user. Returns an empty string if not set.
        """
        settings = cls.load_settings()
        return settings["database"].get("user", "")

    @classmethod
    def get_database_password(cls) -> str:
        """
        Get the database password setting.

        Returns:
            str: The database password. Returns an empty string if not set.
        """
        settings = cls.load_settings()
        return settings["database"].get("password", "")

    @classmethod
    def get_database_name(cls) -> str:
        """
        Get the database name setting.

        Returns:
            str: The database name. Returns an empty string if not set.
        """
        settings = cls.load_settings()
        return settings["database"].get("database", "")
