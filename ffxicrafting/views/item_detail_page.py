import tkinter as tk
from tkinter import ttk
from utils import TreeviewWithSort


class ItemDetailPage(tk.Frame):
    """
    A page displaying detailed information about a specific item.

    This class creates a new tab in the main application notebook, showing
    prices, purchase locations, mob drops, recipes, and profit data.
    """

    def __init__(self, parent: tk.Tk, item_id: int) -> None:
        """
        Initialize the ItemDetailPage.
        Creates a new tab in the parent's notebook and sets up the detail page.

        Args:
            parent (tk.Tk): The parent Tkinter application.
            item_id (int): The ID of the item to display.
        """
        super().__init__(parent)
        self._parent: tk.Tk = parent
        self._previous_tab_index: int = self._parent.notebook.index("current")
        self._item_id: int = item_id

        self._min_cost: int = 1191
        self._max_cost: int = 2357
        self._min_profit_per_synth: int = 100
        self._max_profit_per_synth: int = 200
        self._min_profit_per_storage: int = 1000
        self._max_profit_per_storage: int = 2000
        self._create_detail_page()

    def _create_detail_page(self) -> None:
        """
        Create and layout all widgets for the item detail page.
        """
        self.columnconfigure(0, weight=1, uniform="column")
        self.columnconfigure(1, weight=1, uniform="column")
        self.rowconfigure(0, weight=1, uniform="row")
        self.rowconfigure(1, weight=1, uniform="row")

        self._create_top_left_section()
        self._create_top_right_section()
        self._create_bottom_left_section()
        self._create_bottom_right_section()
        self._add_close_button()

    def _create_top_left_section(self) -> None:
        """
        Create the top left section with item header, auction grid, and recipe select.
        """
        top_left_frame = ttk.Frame(self)
        top_left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        top_left_frame.columnconfigure(0, weight=1)
        top_left_frame.rowconfigure(1, weight=1)

        self._add_item_header(top_left_frame)
        self._add_auction_price_grid(top_left_frame)
        self._add_recipe_select_and_craft_info(top_left_frame)

    def _create_top_right_section(self) -> None:
        """
        Create the top right section with vendor and mob drop treeviews.
        """
        top_right_frame = ttk.Frame(self)
        top_right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        top_right_frame.columnconfigure(0, weight=1)
        top_right_frame.rowconfigure(1, weight=1)
        top_right_frame.rowconfigure(3, weight=1)

        self._add_vendor_and_mob_drop_trees(top_right_frame)

    def _create_bottom_left_section(self) -> None:
        """
        Create the bottom left section with cost per synth label and ingredients tree.
        """
        bottom_left_frame = ttk.Frame(self)
        bottom_left_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        bottom_left_frame.columnconfigure(0, weight=1)
        bottom_left_frame.rowconfigure(1, weight=1)

        self._add_cost_per_synth_labels(bottom_left_frame)
        self._add_ingredients_tree(bottom_left_frame)

    def _create_bottom_right_section(self) -> None:
        """
        Create the bottom right section with profit labels and results tree.
        """
        bottom_right_frame = ttk.Frame(self)
        bottom_right_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        bottom_right_frame.columnconfigure(0, weight=1)
        bottom_right_frame.rowconfigure(1, weight=1)

        self._add_profit_labels(bottom_right_frame)
        self._add_results_tree(bottom_right_frame)

    def _add_item_header(self, parent: ttk.Frame) -> None:
        """
        Add the item name label and craft button.
        """
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, pady=(20, 10))

        item_label = ttk.Label(header_frame, text="Meat Mithkabob", font=("TkDefaultFont", 14, "bold"))
        item_label.grid(row=0, column=0)

        craft_button = ttk.Button(header_frame, text="Craft")
        craft_button.grid(row=1, column=0, pady=(5, 20))

    def _add_auction_price_grid(self, parent: ttk.Frame) -> None:
        """
        Add the 3x2 grid for auction price information.
        """
        price_frame = ttk.Frame(parent)
        price_frame.grid(row=1, column=0, sticky="nsew")
        price_frame.columnconfigure((0, 1, 2, 3), weight=1)

        headers = ["Single", "Stack"]
        for col, header in enumerate(headers):
            ttk.Label(price_frame, text=header, anchor="center").grid(
                row=0, column=col*2, columnspan=2, padx=10, pady=(0, 5))

        # Price row
        ttk.Label(price_frame, text="Price", anchor="w").grid(row=1, column=0, sticky="w", padx=(60, 0), pady=(0, 2))
        ttk.Label(price_frame, text="Price", anchor="w").grid(row=1, column=2, sticky="w", padx=(60, 0), pady=(0, 2))

        price_single = "400-500"  # Replace with variable
        price_stack = "3000-3500"  # Replace with variable
        ttk.Label(price_frame, text=price_single, anchor="e").grid(
            row=1, column=1, sticky="e", padx=(0, 60), pady=(0, 2))
        ttk.Label(price_frame, text=price_stack, anchor="e").grid(
            row=1, column=3, sticky="e", padx=(0, 60), pady=(0, 2))

        # Sell Frequency row
        ttk.Label(price_frame, text="Sell Frequency", anchor="w").grid(
            row=2, column=0, sticky="w", padx=(60, 0), pady=(0, 2))
        ttk.Label(price_frame, text="Sell Frequency", anchor="w").grid(
            row=2, column=2, sticky="w", padx=(60, 0), pady=(0, 2))

        freq_single = "3.6"  # Replace with variable
        freq_stack = "77.9333"  # Replace with variable
        ttk.Label(price_frame, text=freq_single, anchor="e").grid(
            row=2, column=1, sticky="e", padx=(0, 60), pady=(0, 2))
        ttk.Label(price_frame, text=freq_stack, anchor="e").grid(
            row=2, column=3, sticky="e", padx=(0, 60), pady=(0, 2))

    def _add_recipe_select_and_craft_info(self, parent: ttk.Frame) -> None:
        """
        Add recipe selection dropdown and craft information labels.
        """
        info_frame = ttk.Frame(parent)
        info_frame.grid(row=2, column=0, sticky="ew", pady=(5, 0))
        info_frame.columnconfigure(1, weight=1)

        recipes = ["Recipe 1", "Recipe 2", "Recipe 3"]  # Replace with actual recipes
        recipe_select = ttk.Combobox(info_frame, values=recipes, state="readonly")
        recipe_select.set(recipes[0])
        recipe_select.grid(row=0, column=0, padx=10)

        craft_info_frame = ttk.Frame(info_frame)
        craft_info_frame.grid(row=0, column=1, padx=20, sticky="w")

        craft_level = ttk.Label(craft_info_frame, text="Cooking 38")
        craft_level.grid(row=0, column=0, padx=(0, 10))

        craft_tier = ttk.Label(craft_info_frame, text="Tier 3")
        craft_tier.grid(row=0, column=1, padx=(0, 5))

    def _add_vendor_and_mob_drop_trees(self, parent: ttk.Frame) -> None:
        """
        Add vendor and mob drop treeviews.
        """
        # Vendor Tree
        ttk.Label(parent, text="Vendors").grid(row=0, column=0, sticky="w")
        vendor_columns = ("Vendor", "Type", "Location", "Min Cost", "Max Cost")
        self._vendor_tree = TreeviewWithSort(parent, columns=vendor_columns,
                                             show="headings", selectmode="browse", height=5)
        self._configure_treeview_columns(self._vendor_tree, vendor_columns)
        self._vendor_tree.grid(row=1, column=0, sticky="nsew")

        # Mob Drop Tree
        ttk.Label(parent, text="Mob Drops").grid(row=2, column=0, sticky="w")
        mob_columns = ("Mob", "Level", "Location", "Drop Rate")
        self._mob_drop_tree = TreeviewWithSort(parent, columns=mob_columns,
                                               show="headings", selectmode="browse", height=5)
        self._configure_treeview_columns(self._mob_drop_tree, mob_columns)
        self._mob_drop_tree.grid(row=3, column=0, sticky="nsew")

    def _add_cost_per_synth_labels(self, parent: ttk.Frame) -> None:
        """
        Add labels for displaying the cost per synth above the ingredients treeview.
        """
        labels_frame = ttk.Frame(parent)
        labels_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        labels_frame.columnconfigure(0, weight=1)
        labels_frame.columnconfigure(3, weight=1)

        cost_label = ttk.Label(labels_frame, text="Cost / Synth")
        cost_label.grid(row=0, column=1, padx=(0, 10))

        cost_range = f"{self._min_cost} - {self._max_cost}"
        cost_range_label = ttk.Label(labels_frame, text=cost_range)
        cost_range_label.grid(row=0, column=2)

    def _add_ingredients_tree(self, parent: ttk.Frame) -> None:
        """
        Create and configure the treeview for displaying recipe ingredients.
        """
        ingredient_columns = ("Ingredient", "Quantity", "Min Cost", "Max Cost")
        self._ingredients_tree = TreeviewWithSort(
            parent, columns=ingredient_columns, show="headings", selectmode="browse")
        self._configure_treeview_columns(self._ingredients_tree, ingredient_columns)
        self._populate_ingredients_tree()
        self._ingredients_tree.grid(row=1, column=0, sticky="nsew")
        self._ingredients_tree.bind("<Button-1>", self._ingredients_tree.on_click)

    def _add_profit_labels(self, parent: ttk.Frame) -> None:
        """
        Add labels for displaying profit per synth and profit per storage above the results treeview.
        """
        labels_frame = ttk.Frame(parent)
        labels_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        labels_frame.columnconfigure(0, weight=1)
        labels_frame.columnconfigure(1, weight=1)

        # Profit per Synth
        synth_frame = ttk.Frame(labels_frame)
        synth_frame.grid(row=0, column=0, sticky="w")

        ttk.Label(synth_frame, text="Profit / Synth").grid(row=0, column=0, padx=(0, 10))
        profit_per_synth_range = f"{self._min_profit_per_synth} - {self._max_profit_per_synth}"
        profit_per_synth_label = ttk.Label(synth_frame, text=profit_per_synth_range)
        profit_per_synth_label.grid(row=0, column=1)

        # Profit per Storage
        storage_frame = ttk.Frame(labels_frame)
        storage_frame.grid(row=0, column=1, sticky="e")

        ttk.Label(storage_frame, text="Profit / Storage").grid(row=0, column=0, padx=(0, 10))
        profit_per_storage_range = f"{self._min_profit_per_storage} - {self._max_profit_per_storage}"
        profit_per_storage_label = ttk.Label(storage_frame, text=profit_per_storage_range)
        profit_per_storage_label.grid(row=0, column=1)

    def _add_results_tree(self, parent: ttk.Frame) -> None:
        """
        Create and configure the treeview for displaying recipe results.
        """
        result_columns = ("Result", "Proportion", "Profit Contribution")
        self._results_tree = TreeviewWithSort(parent, columns=result_columns, show="headings", selectmode="browse")
        self._configure_treeview_columns(self._results_tree, result_columns)
        self._populate_results_tree()
        self._results_tree.grid(row=1, column=0, sticky="nsew")
        self._results_tree.bind("<Button-1>", self._results_tree.on_click)

    def _add_close_button(self) -> None:
        """
        Add a button to close the item detail page.
        """
        close_button = ttk.Button(self, text="Close", command=self._close_detail_page)
        close_button.grid(row=2, column=0, columnspan=2, pady=(20, 30))

    def _configure_treeview_columns(self, treeview: TreeviewWithSort, columns: list[str]) -> None:
        """
        Configure the columns for a treeview.
        Centers the columns and sets the width to 100 pixels.

        Args:
            treeview (TreeviewWithSort): The treeview to configure.
            columns (list[str]): List of column names to configure.
        """
        for col in columns:
            treeview.heading(col, text=col)
            treeview.column(col, width=100, anchor=tk.CENTER, stretch=True)

    def _populate_ingredients_tree(self) -> None:
        """
        Populate the ingredients treeview with data.
        """
        # Mock data
        self._ingredients_tree.insert("", "end", values=("Fire Crystal", "1", "43", "100"))
        self._ingredients_tree.insert("", "end", values=("Kazham Peppers", "1", "54", "711"))
        self._ingredients_tree.insert("", "end", values=("Mhaura Garlic", "1", "72", "400"))
        self._ingredients_tree.insert("", "end", values=("Wild Onion", "1", "687", "753"))
        self._ingredients_tree.insert("", "end", values=("Cockatrice Meat", "1", "335", "393"))

    def _populate_results_tree(self) -> None:
        """
        Populate the results treeview with data.
        """
        # Mock data
        self._results_tree.insert("", "end", values=("Meat Mithkabob", "88.85%", "43.06%"))
        self._results_tree.insert("", "end", values=("Meat Chiefkabob", "11.15%", "56.94%"))

    def _close_detail_page(self) -> None:
        """
        Close the recipe detail page.

        Removes the current tab from the notebook and returns to the previous tab.
        """
        tab_id = self._parent.notebook.index(self)
        self._parent.notebook.forget(tab_id)
        self._parent.notebook.select(self._previous_tab_index)
