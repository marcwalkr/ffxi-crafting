import tkinter as tk
from tkinter import ttk
from config import SettingsManager
from typing import Union


class SettingsPage(ttk.Frame):
    """
    A page for managing user settings in the FFXI Crafting Tool.

    This class creates a tab in the main application notebook, allowing users to view and modify
    various settings related to profit calculations, skill levels, merchants, conquest, and database connections.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """
        Initialize the SettingsPage.
        Creates a new tab in the parent's notebook and sets up the settings page with various
        categories of settings.

        Args:
            parent (tk.Tk): The parent Tkinter application.
        """
        super().__init__(parent.notebook)
        self._parent: tk.Tk = parent
        self._settings: dict = SettingsManager.load_settings()
        self._thresholds_and_settings: ttk.LabelFrame = None
        self._skill_levels_settings: ttk.LabelFrame = None
        self._merchants_settings: ttk.LabelFrame = None
        self._conquest_settings: ttk.LabelFrame = None
        self._database_settings: ttk.LabelFrame = None

        self._create_settings_page()

    def _create_settings_page(self) -> None:
        """
        Create the main structure of the settings page.

        Adds the settings page to the notebook and creates various categories of settings.
        """
        self._parent.notebook.add(self, text="Settings")
        self._create_settings_categories()

    def _create_settings_categories(self) -> None:
        """
        Create and layout all categories of settings.

        Sets up frames for different setting categories including thresholds and settings,
        skill levels, merchants, conquest, and database settings.
        """
        categories = [
            ("Thresholds and Settings", self._create_thresholds_and_settings),
        ]

        for category_name, create_method in categories:
            frame = ttk.LabelFrame(self, text=category_name)
            frame.pack(fill="x", padx=20, pady=10)
            create_method(frame)

        # Create a frame to hold the bottom section
        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Left column: Skill Levels
        skill_levels_frame = ttk.LabelFrame(bottom_frame, text="Skill Levels")
        skill_levels_frame.pack(side="left", fill="y", padx=(20, 0), pady=5)
        self._create_skill_levels_settings(skill_levels_frame)

        # Middle column: Regional Merchants
        merchants_frame = ttk.LabelFrame(bottom_frame, text="Regional Merchants")
        merchants_frame.pack(side="left", fill="both", padx=20, pady=5)
        self._create_merchants_settings(merchants_frame)

        # Right column: Conquest and Database
        right_column = ttk.Frame(bottom_frame)
        right_column.pack(side="left", fill="both")

        conquest_frame = ttk.LabelFrame(right_column, text="Conquest")
        conquest_frame.pack(fill="x", padx=(0, 20), pady=(0, 20))
        self._create_conquest_settings(conquest_frame)

        bottom_right_frame = ttk.Frame(right_column)
        bottom_right_frame.pack(fill="both", expand=True)

        database_frame = ttk.LabelFrame(bottom_right_frame, text="Database")
        database_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self._create_database_settings(database_frame)

        save_button = ttk.Button(self, text="Save", command=self._save_settings)
        save_button.pack(pady=(10, 40))

    def _create_thresholds_and_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for thresholds and other settings.
        Sets up input fields for profit per synthesis, profit per storage,
        minimum auction list price, and sell frequency.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
        """
        self._thresholds_and_settings = frame
        settings = [
            ("Profit / Synth", 0),
            ("Profit / Storage", 0),
            ("Sell Frequency", 0)
        ]

        # Create a horizontal frame for the number settings
        number_settings_frame = ttk.Frame(frame)
        number_settings_frame.pack(fill="x", padx=20, pady=5)

        self._create_number_settings(number_settings_frame, settings, self._settings.get("thresholds_and_settings", {}))

    def _create_skill_levels_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for crafting skill levels.
        Sets up input fields for various crafting skills.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
        """
        self._skill_levels_settings = frame
        self._create_vertical_number_settings(frame, [
            ("Wood", 0),
            ("Smith", 0),
            ("Gold", 0),
            ("Cloth", 0),
            ("Leather", 0),
            ("Bone", 0),
            ("Alchemy", 0),
            ("Cook", 0)
        ], self._settings.get("skill_levels", {}))

    def _create_merchants_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for regional merchants.
        Sets up dropdown menus for selecting the controlling nation for each region.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
        """
        self._merchants_settings = frame
        merchants = [
            "Aragoneu", "Derfland", "Elshimo Lowlands", "Elshimo Uplands", "Fauregandi",
            "Gustaberg", "Kolshushu", "Kuzotz", "Li'Telor", "Movalpolos", "Norvallen", "Qufim",
            "Ronfaure", "Sarutabaruta", "Tavnazian Archipelago", "Valdeaunia", "Vollbow", "Zulkheim"
        ]
        options = ["San d'Oria", "Bastok", "Windurst", "Beastmen"]

        left_frame = ttk.Frame(frame)
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        right_frame = ttk.Frame(frame)
        right_frame.pack(side="left", fill="y", padx=5, pady=5)

        for i, merchant in enumerate(merchants):
            target_frame = left_frame if i % 2 == 0 else right_frame
            row_frame = ttk.Frame(target_frame)
            row_frame.pack(fill="x", padx=5, pady=2)

            label = ttk.Label(row_frame, text=merchant, width=20, anchor="w")
            label.pack(side="left", padx=(5, 2), pady=2)

            var = tk.StringVar(value=self._settings.get("regional_merchants", {}).get(
                merchant.lower().replace(" ", "_"), "San d'Oria"))
            option_menu = ttk.OptionMenu(row_frame, var, var.get(), *options)
            option_menu.pack(side="left", padx=(2, 5), pady=2)
            option_menu.var = var

    def _create_conquest_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for conquest rankings.
        Sets up dropdown menus for selecting the conquest ranking of each nation.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
        """
        self._conquest_settings = frame
        nations = ["San d'Oria", "Bastok", "Windurst"]
        options = ["1st", "2nd", "3rd"]

        for nation in nations:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", padx=5, pady=2)

            label = ttk.Label(row_frame, text=nation, width=10, anchor="w")
            label.pack(side="left", padx=(5, 2), pady=2)

            var = tk.StringVar(value=self._settings.get("conquest", {}).get(nation.lower().replace("'", ""), "1st"))
            option_menu = ttk.OptionMenu(row_frame, var, var.get(), *options)
            option_menu.pack(side="left", padx=(2, 5), pady=2)
            option_menu.var = var

    def _create_database_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for database connection.
        Sets up input fields for database host, user, password, and database name.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
        """
        self._database_settings = frame
        settings = [
            ("Host", ""),
            ("User", ""),
            ("Password", ""),
            ("Database", "")
        ]
        for setting, default in settings:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            label = ttk.Label(row_frame, text=setting, width=8, anchor="w")
            label.pack(side="left", padx=(5, 2), pady=2)
            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(row_frame, width=15, name=entry_name)
            entry.insert(0, self._settings.get("database", {}).get(entry_name, default))
            entry.pack(side="left", padx=(2, 5), pady=2)

    def _save_settings(self) -> None:
        """
        Save all settings to the configuration file.

        Collects all settings from various categories and saves them using the SettingsManager.
        """
        settings = {
            "thresholds_and_settings": self._get_thresholds_and_settings(),
            "skill_levels": self._get_vertical_number_settings(self._skill_levels_settings),
            "regional_merchants": self._get_regional_merchants_settings(),
            "conquest": self._get_option_menu_settings(self._conquest_settings),
            "database": self._get_string_settings(self._database_settings)
        }
        SettingsManager.save_settings(settings)

    def _get_thresholds_and_settings(self) -> dict:
        """
        Retrieve thresholds and settings including number inputs.

        Returns:
            dict: A dictionary containing thresholds and settings, including numeric values.
        """
        settings = self._get_number_settings(self._thresholds_and_settings)
        return settings

    def _get_number_settings(self, frame: ttk.LabelFrame) -> dict:
        """
        Recursively retrieve number settings from a frame and its child frames.

        Args:
            frame (ttk.LabelFrame): The frame containing number settings.

        Returns:
            dict: A dictionary of setting names and their numeric values (0 if blank).
        """
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                value = child.get()
                settings[label] = self._convert_to_number(value)
            elif isinstance(child, ttk.Frame):
                settings.update(self._get_number_settings(child))  # Recursively check nested frames
        return settings

    def _get_vertical_number_settings(self, frame: ttk.LabelFrame) -> dict:
        """
        Recursively retrieve vertically aligned number settings from a frame and its child frames.

        Args:
            frame (ttk.LabelFrame): The frame containing vertically aligned number settings.

        Returns:
            dict: A dictionary of setting names and their numeric values (0 if blank).
        """
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                value = child.get()
                settings[label] = self._convert_to_number(value)
            elif isinstance(child, ttk.Frame):
                settings.update(self._get_vertical_number_settings(child))  # Recursively check nested frames
        return settings

    def _get_regional_merchants_settings(self) -> dict:
        """
        Retrieve regional merchant settings from the merchants frame.

        Returns:
            dict: A dictionary of merchant names and their selected controlling nations.
        """
        settings = {}
        for child in self._merchants_settings.winfo_children():
            if isinstance(child, ttk.Frame):
                for row_frame in child.winfo_children():
                    if isinstance(row_frame, ttk.Frame):
                        label = row_frame.winfo_children()[0]
                        option_menu = row_frame.winfo_children()[1]
                        merchant_name = label.cget("text").lower().replace(" ", "_")
                        settings[merchant_name] = option_menu.var.get()
        return settings

    def _get_string_settings(self, frame: ttk.LabelFrame) -> dict:
        """
        Recursively retrieve string settings from entry widgets in a frame and its child frames.

        Args:
            frame (ttk.LabelFrame): The frame containing entry widgets.

        Returns:
            dict: A dictionary of setting names and their string values.
        """
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                value = child.get()
                settings[label] = value  # Store as string
            elif isinstance(child, ttk.Frame):
                settings.update(self._get_string_settings(child))  # Recursively check nested frames
        return settings

    def _get_option_menu_settings(self, frame: ttk.LabelFrame) -> dict:
        """
        Retrieve settings from option menus in a frame.

        Args:
            frame (ttk.LabelFrame): The frame containing option menus.

        Returns:
            dict: A dictionary of setting names and their selected values.
        """
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.OptionMenu):
                        label = subchild.master.winfo_children()[0].cget("text").lower().replace("'", "")
                        settings[label] = subchild.var.get()
        return settings

    def _convert_to_number(self, value: str) -> Union[int, float]:
        """
        Convert a string value to a number (int or float).

        Args:
            value (str): The string value to convert.

        Returns:
            Union[int, float]: The converted number. Returns 0 if the input is blank or conversion fails.
        """
        if not value.strip():  # Check if the value is blank or only whitespace
            return 0
        try:
            if "." in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return 0  # Return 0 if conversion fails

    def _create_number_settings(self, frame: ttk.Frame, settings: list[tuple[str, Union[int, float]]],
                                saved_settings: dict) -> None:
        """
        Create number input fields for settings in a horizontal layout.
        Creates labeled entry fields for numeric settings.

        Args:
            frame (ttk.Frame): The frame to contain these settings.
            settings (list[tuple[str, Union[int, float]]]): List of setting names and default values.
            saved_settings (dict): Dictionary of previously saved settings.
        """
        for setting, default in settings:
            setting_frame = ttk.Frame(frame)
            setting_frame.pack(side="left", padx=5, pady=5)

            label = ttk.Label(setting_frame, text=setting)
            label.pack(side="left")

            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(setting_frame, width=10, name=entry_name)
            entry.insert(0, saved_settings.get(entry_name, default))
            entry.pack(side="left", padx=(5, 0))

    def _create_vertical_number_settings(self, frame: ttk.LabelFrame, settings: list[tuple[str, Union[int, float]]],
                                         saved_settings: dict) -> None:
        """
        Create vertically aligned number input fields for settings.
        Creates vertically aligned labeled entry fields for numeric settings.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
            settings (list[tuple[str, Union[int, float]]]): List of setting names and default values.
            saved_settings (dict): Dictionary of previously saved settings.
        """
        for setting, default in settings:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            label = ttk.Label(row_frame, text=setting)
            label.pack(side="left", padx=5, pady=5)
            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(row_frame, width=10, name=entry_name)
            entry.insert(0, saved_settings.get(entry_name, default))
            entry.pack(side="right", padx=5, pady=5)

    def _create_merchants_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for regional merchants in a two-column layout.
        Creates a two-column layout of option menus for selecting the controlling nation for each region.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
        """
        self._merchants_settings = frame
        merchants = [
            "Aragoneu", "Derfland", "Elshimo Lowlands", "Elshimo Uplands", "Fauregandi",
            "Gustaberg", "Kolshushu", "Kuzotz", "Li'Telor", "Movalpolos", "Norvallen", "Qufim",
            "Ronfaure", "Sarutabaruta", "Tavnazian Archipelago", "Valdeaunia", "Vollbow", "Zulkheim"
        ]
        options = ["San d'Oria", "Bastok", "Windurst", "Beastmen"]

        left_frame = ttk.Frame(frame)
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        right_frame = ttk.Frame(frame)
        right_frame.pack(side="left", fill="y", padx=5, pady=5)

        for i, merchant in enumerate(merchants):
            target_frame = left_frame if i % 2 == 0 else right_frame
            row_frame = ttk.Frame(target_frame)
            row_frame.pack(fill="x", padx=5, pady=2)

            label = ttk.Label(row_frame, text=merchant, width=20, anchor="w")
            label.pack(side="left", padx=(5, 2), pady=2)

            var = tk.StringVar(value=self._settings.get("regional_merchants", {}).get(
                merchant.lower().replace(" ", "_"), "San d'Oria"))
            option_menu = ttk.OptionMenu(row_frame, var, var.get(), *options)
            option_menu.pack(side="left", padx=(2, 5), pady=2)
            option_menu.var = var

    def _create_string_settings(self, frame: ttk.LabelFrame, settings: list[tuple[str, str]],
                                saved_settings: dict) -> None:
        """
        Create string settings using labeled entry widgets.
        Creates labeled entry widgets for string settings.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
            settings (list[tuple[str, str]]): List of tuples containing setting names and default values.
            saved_settings (dict): Dictionary of previously saved settings.
        """
        for setting, default in settings:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            label = ttk.Label(row_frame, text=setting)
            label.pack(side="left", padx=5, pady=5)
            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(row_frame, width=20, name=entry_name)
            entry.insert(0, saved_settings.get(entry_name, default))
            entry.pack(side="right", padx=5, pady=5)
