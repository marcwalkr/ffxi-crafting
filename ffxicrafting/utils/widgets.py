import re
import tkinter as tk
from tkinter import ttk


class TreeviewWithSort(ttk.Treeview):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.init_sorting()

    def init_sorting(self):
        for col in self["columns"]:
            self.heading(col, text=col, command=lambda c=col: self.sort_by(c, False))

    def sort_by(self, col, descending):
        def convert(value):
            if value == "":
                return float('-inf') if descending else float('inf')
            if value == "-":
                return float('-inf') if descending else float('inf')
            try:
                return float(value) if '.' in value else int(value)
            except ValueError:
                return value.lower()  # Convert strings to lowercase for sorting

        def natural_keys(text):
            # Split the text into segments that are either digit or non-digit
            return [convert(c) for c in re.split(r'(-?\d+(?:\.\d+)?|\D+)', text) if c]

        # Extract the data with the natural keys
        data = [(natural_keys(self.set(child, col)), child) for child in self.get_children('')]
        # Sort the data based on the extracted keys
        data.sort(key=lambda x: x[0], reverse=descending)

        # Reorder the items in the Treeview
        for idx, (val, child) in enumerate(data):
            self.move(child, "", idx)

        # Update the heading so it sorts in the opposite order next time
        self.heading(col, command=lambda: self.sort_by(col, not descending))

    def on_click(self, event: tk.Event) -> None:
        """
        Handle clicks on the treeview to clear selection if clicking on empty space or heading.

        Args:
            event (tk.Event): The click event on the treeview.
        """
        region = self.identify("region", event.x, event.y)
        if region in ("nothing", "heading"):
            self.selection_remove(self.selection())

    def clear(self) -> None:
        """Clear all items from the treeview."""
        for item in self.get_children():
            self.delete(item)
