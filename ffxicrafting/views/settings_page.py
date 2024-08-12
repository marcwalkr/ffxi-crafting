import tkinter as tk
from tkinter import ttk
from config import SettingsManager
from typing import Union


class SettingsPage(ttk.Frame):
    """
    A page for managing user settings in the FFXI Crafting Tool.

    This class creates a tab in the main application notebook, allowing users to view and modify
    various settings related to merchants, conquest, and database connections.
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

        Sets up frames for different setting categories including merchants, conquest, and database settings.
        """
        # Create a frame to hold all settings
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=200, pady=50)

        # Regional Merchants
        merchants_frame = ttk.LabelFrame(main_frame, text="Regional Merchants")
        merchants_frame.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=5)
        self._create_merchants_settings(merchants_frame)

        # Right column: Conquest and Database
        right_column = ttk.Frame(main_frame)
        right_column.pack(side="left", fill="both", expand=True)

        conquest_frame = ttk.LabelFrame(right_column, text="Conquest")
        conquest_frame.pack(fill="x", pady=(0, 10))
        self._create_conquest_settings(conquest_frame)

        database_frame = ttk.LabelFrame(right_column, text="Database")
        database_frame.pack(fill="both", expand=True)
        self._create_database_settings(database_frame)

        save_button = ttk.Button(self, text="Save", command=self._save_settings)
        save_button.pack(pady=(0, 40))

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
        current_settings = SettingsManager.load_settings()

        new_settings = {
            "regional_merchants": self._get_regional_merchants_settings(),
            "conquest": self._get_option_menu_settings(self._conquest_settings),
            "database": self._get_string_settings(self._database_settings)
        }

        current_settings.update(new_settings)
        SettingsManager.save_settings(current_settings)

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
