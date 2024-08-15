from tkinter import ttk
from typing import Union


def clamp(n: float, minn: float, maxn: float) -> float:
    """
    Constrain a number within a specified range.

    Ensures that the given number "n" falls within the range defined by
    "minn" and "maxn". If "n" is less than "minn", it returns "minn".
    If "n" is greater than "maxn", it returns "maxn". Otherwise, it returns "n".

    Args:
        n (float): The number to be clamped.
        minn (float): The minimum allowed value.
        maxn (float): The maximum allowed value.

    Returns:
        float: The clamped value of "n", which will be between "minn" and "maxn", inclusive.
    """
    return max(min(maxn, n), minn)


def convert_to_number(value: str) -> Union[int, float]:
    """
    Convert a string value to a number (int or float).

    Args:
        value (str): The string value to convert.

    Returns:
        Union[int, float]: The converted number. Returns 0 if the input is blank
                           or conversion fails.
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


def create_number_settings(frame: ttk.Frame, settings: list[tuple[str, Union[int, float]]],
                           saved_settings: dict, orientation: str = "horizontal") -> None:
    """
    Create number input fields for a group of settings.

    This function creates a label and an entry widget for each setting, arranged
    either horizontally or vertically within the given frame using the grid layout.

    Args:
        frame (ttk.Frame): The parent frame to contain these settings.
        settings (list[tuple[str, Union[int, float]]]): A list of tuples, each containing
            the setting name and its default value.
        saved_settings (dict): A dictionary of previously saved settings to populate
            the input fields.
        orientation (str): The orientation of the settings, either "horizontal" or "vertical".
    """
    for i, (setting, default) in enumerate(settings):
        row = i if orientation == "vertical" else 0
        col = 0 if orientation == "vertical" else i * 2

        label = ttk.Label(frame, text=setting, anchor="e")
        label.grid(row=row, column=col, padx=(0, 20), pady=2, sticky="w")

        entry_name = setting.lower().replace(" ", "_")
        entry = ttk.Entry(frame, width=10, name=entry_name)
        entry.insert(0, saved_settings.get(entry_name, default))
        entry.grid(row=row, column=col + 1, padx=(0, 10), pady=2, sticky="w")

    # Configure grid to expand properly
    if orientation == "horizontal":
        frame.grid_columnconfigure(len(settings) * 2 - 1, weight=1)
    else:
        frame.grid_columnconfigure(1, weight=1)


def get_number_settings(frame: ttk.Widget) -> dict:
    """
    Recursively retrieve number settings from a frame and its child frames.

    This function traverses the widget hierarchy within the given frame,
    collecting values from Entry widgets and converting them to numbers.

    Args:
        frame (ttk.Widget): The frame or widget containing number settings.

    Returns:
        dict: A dictionary of setting names and their numeric values.
    """
    settings = {}
    for child in frame.winfo_children():
        if isinstance(child, ttk.Entry):
            label = child._name.split(".")[-1]
            value = child.get()
            settings[label] = convert_to_number(value)
        elif isinstance(child, (ttk.Frame, ttk.LabelFrame)):
            settings.update(get_number_settings(child))  # Recursively check nested frames
    return settings
