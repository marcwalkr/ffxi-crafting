import tkinter as tk
from tkinter import ttk
from config import SettingsManager
from typing import Union


class SettingsPage(ttk.Frame):
    """
    A page for managing user settings in the FFXI Crafting Tool.

    This class creates a tab in the main application notebook, allowing users to view and modify
    various settings related to profit calculations, synthesis, skill levels, merchants, conquest,
    guilds, and database connections.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """
        Initialize the SettingsPage.

        Args:
            parent (tk.Tk): The parent Tkinter application.

        Creates a new tab in the parent's notebook and sets up the settings page with various
        categories of settings.
        """
        super().__init__(parent.notebook)
        self._parent: tk.Tk = parent
        self._settings: dict = SettingsManager.load_settings()

        self._profit_table_settings: ttk.LabelFrame = None
        self._synth_settings: ttk.LabelFrame = None
        self._skill_levels_settings: ttk.LabelFrame = None
        self._merchants_settings: ttk.LabelFrame = None
        self._conquest_settings: ttk.LabelFrame = None
        self._guilds_settings: ttk.LabelFrame = None
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

        Sets up frames for different setting categories including profit table, synthesis,
        skill levels, merchants, conquest, guilds, and database settings.
        """
        categories = [
            ("Profit Table", self._create_profit_table_settings),
            ("Synth", self._create_synth_settings),
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
        skill_levels_frame.pack(side="left", fill="y", padx=(40, 0), pady=5)
        self._create_skill_levels_settings(skill_levels_frame)

        # Middle column: Regional Merchants
        merchants_frame = ttk.LabelFrame(bottom_frame, text="Regional Merchants")
        merchants_frame.pack(side="left", fill="both", expand=True, padx=60, pady=5)
        self._create_merchants_settings(merchants_frame)

        # Right column: Conquest, Guild Merchants, and Database
        right_column = ttk.Frame(bottom_frame)
        right_column.pack(side="left", fill="both")

        conquest_frame = ttk.LabelFrame(right_column, text="Conquest")
        conquest_frame.pack(fill="x", padx=(0, 20), pady=(0, 20))
        self._create_conquest_settings(conquest_frame)

        bottom_right_frame = ttk.Frame(right_column)
        bottom_right_frame.pack(fill="both", expand=True)

        guilds_frame = ttk.LabelFrame(bottom_right_frame, text="Guild Merchants")
        guilds_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self._create_guilds_settings(guilds_frame)

        database_frame = ttk.LabelFrame(bottom_right_frame, text="Database")
        database_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self._create_database_settings(database_frame)

        save_button = ttk.Button(self, text="Save", command=self._save_settings)
        save_button.pack(pady=(10, 40))

    def _create_profit_table_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for the profit table.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.

        Sets up input fields for profit per synthesis, profit per storage,
        minimum auction list price, and sell frequency.
        """
        self._profit_table_settings = frame
        settings = [
            ("Profit / Synth", 0),
            ("Profit / Storage", 0),
            ("Min Auction List Price", 0),
            ("Sell Frequency", 0)
        ]
        self._create_number_settings(frame, settings, self._settings.get("profit_table", {}))

    def _create_synth_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for synthesis.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.

        Sets up input fields for skill look ahead and simulation trials,
        as well as a checkbox for crafting ingredients.
        """
        self._synth_settings = frame
        settings = [
            ("Skill Look Ahead", 0),
            ("Simulation Trials", 1000)
        ]
        self._create_number_settings(frame, settings, self._settings.get("synth", {}))

        craft_ingredients_var = tk.BooleanVar(value=self._settings.get(
            "profit_table", {}).get("craft_ingredients", False))
        craft_ingredients_cb = ttk.Checkbutton(frame, text="Craft Ingredients", variable=craft_ingredients_var,
                                               style="Custom.TCheckbutton")
        craft_ingredients_cb.pack(side="left", padx=20, pady=5)
        craft_ingredients_cb.var = craft_ingredients_var

    def _create_skill_levels_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for crafting skill levels.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.

        Sets up input fields for various crafting skills.
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

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.

        Sets up dropdown menus for selecting the controlling nation for each region.
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

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.

        Sets up dropdown menus for selecting the conquest ranking of each nation.
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

    def _create_guilds_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for guild merchants.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.

        Sets up checkboxes for each crafting guild and the Tenshodo.
        """
        self._guilds_settings = frame
        guilds = [
            "Alchemy", "Bonecraft", "Clothcraft", "Cooking", "Fishing",
            "Goldsmithing", "Leathercraft", "Smithing", "Woodworking", "Tenshodo"
        ]
        for guild in guilds:
            var = tk.BooleanVar(value=self._settings.get("guilds", {}).get(guild.lower(), False))
            checkbutton = ttk.Checkbutton(frame, text=guild, variable=var, style="Custom.TCheckbutton")
            checkbutton.pack(anchor="w", padx=5, pady=2)
            checkbutton.var = var

    def _create_database_settings(self, frame: ttk.LabelFrame) -> None:
        """
        Create settings for database connection.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.

        Sets up input fields for database host, user, password, and database name.
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
            "profit_table": self._get_number_settings(self._profit_table_settings),
            "synth": self._get_synth_settings(),
            "skill_levels": self._get_vertical_number_settings(self._skill_levels_settings),
            "regional_merchants": self._get_regional_merchants_settings(),
            "conquest": self._get_option_menu_settings(self._conquest_settings),
            "guilds": self._get_boolean_settings(self._guilds_settings),
            "database": self._get_string_settings(self._database_settings)
        }
        SettingsManager.save_settings(settings)

    def _get_synth_settings(self) -> dict:
        """
        Retrieve synthesis settings including number settings and checkbox values.

        Returns:
            dict: A dictionary containing synthesis settings, including 'craft_ingredients' boolean.
        """
        settings = self._get_number_settings(self._synth_settings)
        # Add the checkbox value
        for child in self._synth_settings.winfo_children():
            if isinstance(child, ttk.Checkbutton) and child.cget("text") == "Craft Ingredients":
                settings["craft_ingredients"] = child.var.get()
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

    def _get_boolean_settings(self, frame: ttk.LabelFrame) -> dict:
        """
        Recursively retrieve boolean settings from checkbuttons in a frame and its child frames.

        Args:
            frame (ttk.LabelFrame): The frame containing checkbuttons.

        Returns:
            dict: A dictionary of setting names and their boolean values.
        """
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Checkbutton):
                label = child.cget("text").lower().replace(" ", "_")
                settings[label] = child.instate(['selected'])
            elif isinstance(child, ttk.Frame):
                settings.update(self._get_boolean_settings(child))  # Recursively check nested frames
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

    def _create_number_settings(self, frame: ttk.LabelFrame, settings: list[tuple[str, Union[int, float]]],
                                saved_settings: dict) -> None:
        """
        Create number input fields for settings.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
            settings (list[tuple[str, Union[int, float]]]): List of setting names and default values.
            saved_settings (dict): Dictionary of previously saved settings.

        Creates labeled entry fields for numeric settings.
        """
        for setting, default in settings:
            label = ttk.Label(frame, text=setting)
            label.pack(side="left", padx=5, pady=5)
            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(frame, width=10, name=entry_name)
            entry.insert(0, saved_settings.get(entry_name, default))
            entry.pack(side="left", padx=5, pady=5)

    def _create_vertical_number_settings(self, frame: ttk.LabelFrame, settings: list[tuple[str, Union[int, float]]],
                                         saved_settings: dict) -> None:
        """
        Create vertically aligned number input fields for settings.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
            settings (list[tuple[str, Union[int, float]]]): List of setting names and default values.
            saved_settings (dict): Dictionary of previously saved settings.

        Creates vertically aligned labeled entry fields for numeric settings.
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

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.

        Creates a two-column layout of option menus for selecting the controlling nation for each region.
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

    def _create_two_column_boolean_settings(self, frame: ttk.LabelFrame, settings: list[str],
                                            saved_settings: dict) -> None:
        """
        Create a two-column layout of boolean settings using checkbuttons.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
            settings (list[str]): List of setting names.
            saved_settings (dict): Dictionary of previously saved settings.

        Creates a two-column layout of checkbuttons for boolean settings.
        """
        left_frame = ttk.Frame(frame)
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        right_frame = ttk.Frame(frame)
        right_frame.pack(side="left", fill="y", padx=5, pady=5)

        for i, setting in enumerate(settings):
            target_frame = left_frame if i % 2 == 0 else right_frame
            var = tk.BooleanVar(value=saved_settings.get(setting.lower().replace(" ", "_"), False))
            checkbutton = ttk.Checkbutton(target_frame, text=setting, variable=var, style="Custom.TCheckbutton")
            checkbutton.pack(anchor="w", padx=5, pady=2)
            checkbutton.var = var

    def _create_string_settings(self, frame: ttk.LabelFrame, settings: list[tuple[str, str]],
                                saved_settings: dict) -> None:
        """
        Create string settings using labeled entry widgets.

        Args:
            frame (ttk.LabelFrame): The frame to contain these settings.
            settings (list[tuple[str, str]]): List of tuples containing setting names and default values.
            saved_settings (dict): Dictionary of previously saved settings.

        Creates labeled entry widgets for string settings.
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
