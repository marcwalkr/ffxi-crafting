import tkinter as tk
from tkinter import ttk
from config.settings_manager import SettingsManager


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
            frame.pack(fill="x", padx=10, pady=5)
            create_method(frame)

        skill_and_merchants_frame = ttk.Frame(self)
        skill_and_merchants_frame.pack(fill="x", padx=10, pady=5)

        skill_levels_frame = ttk.LabelFrame(skill_and_merchants_frame, text="Skill Levels")
        skill_levels_frame.pack(side="left", fill="x", padx=10, pady=5)
        self.create_skill_levels_settings(skill_levels_frame)

        merchants_frame = ttk.LabelFrame(skill_and_merchants_frame, text="Merchants")
        merchants_frame.pack(side="left", fill="x", padx=10, pady=5)
        self.create_merchants_settings(merchants_frame)

        save_button = ttk.Button(self, text="Save", command=self.save_settings)
        save_button.pack(pady=10)

    def create_profit_table_settings(self, frame):
        self.profit_table_settings = frame
        settings = [
            ("Profit / Synth", 0),
            ("Profit / Storage", 0),
            ("Min Sell Price", 0)
        ]
        self.create_number_settings(frame, settings, self.settings.get("profit_table", {}))

    def create_synth_settings(self, frame):
        self.synth_settings = frame
        settings = [
            ("Skill Look Ahead", 0),
            ("Simulation Trials", 1000)
        ]
        self.create_number_settings(frame, settings, self.settings.get("synth", {}))

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
        self.create_two_column_boolean_settings(frame, [
            "Guilds", "Aragoneu", "Derfland", "Elshimo Lowlands", "Elshimo Uplands", "Fauregandi",
            "Gustaberg", "Kolshushu", "Kuzotz", "Li'Telor", "Movalpolos", "Norvallen", "Qufim",
            "Ronfaure", "Sarutabaruta", "Tavnazian Archipelago", "Valdeaunia", "Vollbow", "Zulkheim"
        ], self.settings.get("merchants", {}))

    def save_settings(self):
        settings = {
            "profit_table": self.get_number_settings(self.profit_table_settings),
            "synth": self.get_number_settings(self.synth_settings),
            "skill_levels": self.get_vertical_number_settings(self.skill_levels_settings),
            "merchants": self.get_boolean_settings(self.merchants_settings)
        }
        SettingsManager.save_settings(settings)

    def get_number_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                settings[label] = child.get()
            elif isinstance(child, ttk.Frame):
                settings.update(self.get_number_settings(child))  # Recursively check nested frames
        return settings

    def get_vertical_number_settings(self, frame):
        settings = {}
        for child in frame.winfo_children():
            if isinstance(child, ttk.Entry):
                label = child._name.split(".")[-1]
                settings[label] = child.get()
            elif isinstance(child, ttk.Frame):
                settings.update(self.get_vertical_number_settings(child))  # Recursively check nested frames
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
