import re
import tkinter as tk
from tkinter import ttk


class TreeviewWithSort(ttk.Treeview):
    """
    A custom Treeview widget with built-in sorting functionality.

    This class extends the ttk.Treeview widget to add column sorting capabilities,
    including natural sorting for alphanumeric data. It also provides methods for
    handling click events and clearing the treeview.
    """

    def __init__(self, master: tk.Tk, **kwargs):
        """
        Initialize the TreeviewWithSort widget.

        Args:
            master (tk.Tk): The parent widget.
            **kwargs: Additional keyword arguments to be passed to the ttk.Treeview constructor.
        """
        super().__init__(master, **kwargs)
        self._init_sorting()

    def _init_sorting(self):
        """
        Initialize the sorting functionality for all columns.

        This method sets up click handlers on column headings to enable sorting.
        """
        for col in self["columns"]:
            self.heading(col, text=col, command=lambda c=col: self._sort_by(c, False))

    def _sort_by(self, col: str, descending: bool) -> None:
        """
        Sort the treeview by a specific column.

        This method implements a natural sort algorithm, which correctly sorts
        alphanumeric strings (e.g., "item10" comes after "item2").

        Args:
            col (str): The column to sort by.
            descending (bool): If True, sort in descending order; if False, in ascending order.
        """
        def _convert(value: str) -> float | int | str:
            """
            Convert a string value to an appropriate type for sorting.

            Args:
                value (str): The value to convert.

            Returns:
                float | int | str: The converted value.
            """
            if value == "":
                return float('-inf') if descending else float('inf')
            if value == "-":
                return float('-inf') if descending else float('inf')
            try:
                return float(value) if '.' in value else int(value)
            except ValueError:
                return value.lower()  # Convert strings to lowercase for sorting

        def _natural_keys(text: str) -> list[float | int | str]:
            """
            Split text into natural sort keys.

            Args:
                text (str): The text to split into keys.

            Returns:
                list[float | int | str]: A list of keys for natural sorting.
            """
            return [_convert(c) for c in re.split(r'(-?\d+(?:\.\d+)?|\D+)', text) if c]

        # Extract the data with the natural keys
        data = [(_natural_keys(self.set(child, col)), child) for child in self.get_children('')]
        # Sort the data based on the extracted keys
        data.sort(key=lambda x: x[0], reverse=descending)

        # Reorder the items in the Treeview
        for idx, (val, child) in enumerate(data):
            self.move(child, "", idx)

        # Update the heading so it sorts in the opposite order next time
        self.heading(col, command=lambda: self._sort_by(col, not descending))

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
