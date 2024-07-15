import re
from tkinter import ttk


class TreeviewWithSort(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self._init_sorting()

    def _init_sorting(self):
        for col in self["columns"]:
            self.heading(col, text=col, command=lambda c=col: self._sort_by(c, False))

    def _sort_by(self, col, descending):
        def convert(value):
            if value == "":
                return float('-inf') if descending else float('inf')
            try:
                return float(value)
            except ValueError:
                return value

        def natural_keys(text):
            return [convert(c) if c.isdigit() else c for c in re.split(r'(\d+)', text)]

        data = [(natural_keys(self.set(child, col)), child) for child in self.get_children('')]
        data.sort(reverse=descending)

        for idx, (val, child) in enumerate(data):
            self.move(child, "", idx)

        self.heading(col, command=lambda: self._sort_by(col, not descending))
