import tkinter as tk
from tkinter import ttk
from config import SettingsManager


class SettingsPage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent.notebook)
        self.parent = parent
        self.settings = SettingsManager.load_settings()
        self.create_settings_page()

    def create_settings_page(self):
        self.parent.notebook.add(self, text="Settings")
        self.create_settings_categories()

    def create_settings_categories(self):
        categories = [
            ("Profit Table", self.create_profit_table_settings),
            ("Synth", self.create_synth_settings),
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
        self.create_skill_levels_settings(skill_levels_frame)

        # Middle column: Regional Merchants
        merchants_frame = ttk.LabelFrame(bottom_frame, text="Regional Merchants")
        merchants_frame.pack(side="left", fill="both", expand=True, padx=60, pady=5)
        self.create_merchants_settings(merchants_frame)

        # Right column: Conquest, Guild Merchants, and Database
        right_column = ttk.Frame(bottom_frame)
        right_column.pack(side="left", fill="both")

        conquest_frame = ttk.LabelFrame(right_column, text="Conquest")
        conquest_frame.pack(fill="x", padx=(0, 20), pady=(0, 20))
        self.create_conquest_settings(conquest_frame)

        bottom_right_frame = ttk.Frame(right_column)
        bottom_right_frame.pack(fill="both", expand=True)

        guilds_frame = ttk.LabelFrame(bottom_right_frame, text="Guild Merchants")
        guilds_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.create_guilds_settings(guilds_frame)

        database_frame = ttk.LabelFrame(bottom_right_frame, text="Database")
        database_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        self.create_database_settings(database_frame)

        save_button = ttk.Button(self, text="Save", command=self.save_settings)
        save_button.pack(pady=(10, 40))

    def create_profit_table_settings(self, frame):
        self.profit_table_settings = frame
        settings = [
            ("Profit / Synth", 0),
            ("Profit / Storage", 0),
            ("Min Sell Price", 0),
            ("Sell Frequency", 0)
        ]
        self.create_number_settings(frame, settings, self.settings.get("profit_table", {}))

    def create_synth_settings(self, frame):
        self.synth_settings = frame
        settings = [
            ("Skill Look Ahead", 0),
            ("Simulation Trials", 1000)
        ]
        self.create_number_settings(frame, settings, self.settings.get("synth", {}))

        craft_ingredients_var = tk.BooleanVar(value=self.settings.get(
            "profit_table", {}).get("craft_ingredients", False))
        craft_ingredients_cb = ttk.Checkbutton(frame, text="Craft Ingredients", variable=craft_ingredients_var,
                                               style="Custom.TCheckbutton")
        craft_ingredients_cb.pack(side="left", padx=20, pady=5)
        craft_ingredients_cb.var = craft_ingredients_var

    def create_skill_levels_settings(self, frame):
        self.skill_levels_settings = frame
        self.create_vertical_number_settings(frame, [
            ("Wood", 0),
            ("Smith", 0),
            ("Gold", 0),
            ("Cloth", 0),
            ("Leather", 0),
            ("Bone", 0),
            ("Alchemy", 0),
            ("Cook", 0)
        ], self.settings.get("skill_levels", {}))

    def create_merchants_settings(self, frame):
        self.merchants_settings = frame
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

            var = tk.StringVar(value=self.settings.get("regional_merchants", {}).get(
                merchant.lower().replace(" ", "_"), "San d'Oria"))
            option_menu = ttk.OptionMenu(row_frame, var, var.get(), *options)
            option_menu.pack(side="left", padx=(2, 5), pady=2)
            option_menu.var = var

    def create_conquest_settings(self, frame):
        self.conquest_settings = frame
        conquest_ranks = ["1st", "2nd", "3rd"]
        options = ["San d'Oria", "Bastok", "Windurst"]

        for rank in conquest_ranks:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", padx=5, pady=2)

            label = ttk.Label(row_frame, text=rank, width=5)
            label.pack(side="left", padx=(5, 2), pady=2)

            var = tk.StringVar(value=self.settings.get("conquest", {}).get(rank.lower(), "San d'Oria"))
            option_menu = ttk.OptionMenu(row_frame, var, var.get(), *options)
            option_menu.pack(side="left", padx=(2, 5), pady=2)
            option_menu.var = var

    def create_guilds_settings(self, frame):
        self.guilds_settings = frame
        guilds = [
            "Alchemy", "Bonecraft", "Clothcraft", "Cooking", "Fishing",
            "Goldsmithing", "Leathercraft", "Smithing", "Woodworking", "Tenshodo"
        ]
        for guild in guilds:
            var = tk.BooleanVar(value=self.settings.get("guilds", {}).get(guild.lower(), False))
            checkbutton = ttk.Checkbutton(frame, text=guild, variable=var, style="Custom.TCheckbutton")
            checkbutton.pack(anchor="w", padx=5, pady=2)
            checkbutton.var = var

    def create_database_settings(self, frame):
        self.database_settings = frame
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
            entry.insert(0, self.settings.get("database", {}).get(entry_name, default))
            entry.pack(side="left", padx=(2, 5), pady=2)

    def save_settings(self):
        settings = {
            "profit_table": self.get_number_settings(self.profit_table_settings),
            "synth": self.get_synth_settings(),
            "skill_levels": self.get_vertical_number_settings(self.skill_levels_settings),
            "regional_merchants": self.get_regional_merchants_settings(),
            "conquest": self.get_option_menu_settings(self.conquest_settings),
            "guilds": self.get_boolean_settings(self.guilds_settings),
            "database": self.get_string_settings(self.database_settings)
        }
        SettingsManager.save_settings(settings)

    def get_synth_settings(self):
        settings = self.get_number_settings(self.synth_settings)
        # Add the checkbox value
        for child in self.synth_settings.winfo_children():
            if isinstance(child, ttk.Checkbutton) and child.cget("text") == "Craft Ingredients":
                settings["craft_ingredients"] = child.var.get()
        return settings

    def get_number_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                value = child.get()
                settings[label] = self.convert_to_number(value)
            elif isinstance(child, ttk.Frame):
                settings.update(self.get_number_settings(child))  # Recursively check nested frames
        return settings

    def get_vertical_number_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                value = child.get()
                settings[label] = self.convert_to_number(value)
            elif isinstance(child, ttk.Frame):
                settings.update(self.get_vertical_number_settings(child))  # Recursively check nested frames
        return settings

    def get_regional_merchants_settings(self):
        settings = {}
        for child in self.merchants_settings.winfo_children():
            if isinstance(child, ttk.Frame):
                for row_frame in child.winfo_children():
                    if isinstance(row_frame, ttk.Frame):
                        label = row_frame.winfo_children()[0]
                        option_menu = row_frame.winfo_children()[1]
                        merchant_name = label.cget("text").lower().replace(" ", "_")
                        settings[merchant_name] = option_menu.var.get()
        return settings

    def get_boolean_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Checkbutton):
                label = child.cget("text").lower().replace(" ", "_")
                settings[label] = child.instate(['selected'])
            elif isinstance(child, ttk.Frame):
                settings.update(self.get_boolean_settings(child))  # Recursively check nested frames
        return settings

    def get_string_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                value = child.get()
                settings[label] = value  # Store as string
            elif isinstance(child, ttk.Frame):
                settings.update(self.get_string_settings(child))  # Recursively check nested frames
        return settings

    def get_option_menu_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Frame):
                for subchild in child.winfo_children():
                    if isinstance(subchild, ttk.OptionMenu):
                        label = subchild.master.winfo_children()[0].cget("text").lower().replace(" ", "_")
                        settings[label] = subchild.var.get()
        return settings

    def convert_to_number(self, value):
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            return value  # Return as is if conversion fails

    def create_number_settings(self, frame, settings, saved_settings):
        for setting, default in settings:
            label = ttk.Label(frame, text=setting)
            label.pack(side="left", padx=5, pady=5)
            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(frame, width=10, name=entry_name)
            entry.insert(0, saved_settings.get(entry_name, default))
            entry.pack(side="left", padx=5, pady=5)

    def create_vertical_number_settings(self, frame, settings, saved_settings):
        for setting, default in settings:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            label = ttk.Label(row_frame, text=setting)
            label.pack(side="left", padx=5, pady=5)
            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(row_frame, width=10, name=entry_name)
            entry.insert(0, saved_settings.get(entry_name, default))
            entry.pack(side="right", padx=5, pady=5)

    def create_merchants_settings(self, frame):
        self.merchants_settings = frame
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

            var = tk.StringVar(value=self.settings.get("regional_merchants", {}).get(
                merchant.lower().replace(" ", "_"), "San d'Oria"))
            option_menu = ttk.OptionMenu(row_frame, var, var.get(), *options)
            option_menu.pack(side="left", padx=(2, 5), pady=2)
            option_menu.var = var

    def create_two_column_boolean_settings(self, frame, settings, saved_settings):
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

    def create_string_settings(self, frame, settings, saved_settings):
        for setting, default in settings:
            row_frame = ttk.Frame(frame)
            row_frame.pack(fill="x", padx=5, pady=2)
            label = ttk.Label(row_frame, text=setting)
            label.pack(side="left", padx=5, pady=5)
            entry_name = setting.lower().replace(" ", "_")
            entry = ttk.Entry(row_frame, width=20, name=entry_name)
            entry.insert(0, saved_settings.get(entry_name, default))
            entry.pack(side="right", padx=5, pady=5)
