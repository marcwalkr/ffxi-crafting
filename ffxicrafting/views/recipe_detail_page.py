import tkinter as tk
from tkinter import ttk
from entities import SimulationData
from utils import TreeviewWithSort


class RecipeDetailPage(ttk.Frame):
    """
    A page displaying detailed information about a specific crafting recipe.

    This class creates a new tab in the main application notebook, showing
    ingredients, costs, and results for a selected recipe.
    """

    def __init__(self, parent: tk.Tk, simulation_data: SimulationData) -> None:
        """
        Initialize the RecipeDetailPage.
        Creates a new tab in the parent's notebook and sets up the detail page.

        Args:
            parent (tk.Tk): The parent Tkinter application.
            profit_data (ProfitData): The profit data object to display the values of.
        """
        super().__init__(parent.notebook)
        self._parent: tk.Tk = parent
        self._previous_tab_index: int = self._parent.notebook.index("current")
        self._ingredients_tree: TreeviewWithSort = None
        self._results_tree: TreeviewWithSort = None
        self._simulation_data: SimulationData = simulation_data
        self._cost_per_synth_value_label: ttk.Label = None

        self._create_detail_page()

    def _create_detail_page(self) -> None:
        """
        Create and layout all widgets for the recipe detail page.

        Sets up the recipe label, ingredients tree, cost per synth frame,
        results tree, and close button.
        """
        self._add_recipe_label(self._simulation_data.recipe.result_name)
        self._add_ingredients_tree()
        self._add_cost_per_synth_frame()
        self._add_results_tree()
        self._add_close_button()

    def _add_recipe_label(self, text: str) -> None:
        """
        Add a label displaying the recipe name.

        Args:
            text (str): The name of the recipe to display.
        """
        recipe_label = ttk.Label(self, text=text)
        recipe_label.pack(pady=10)

    def _add_ingredients_tree(self) -> None:
        """
        Create and configure the treeview for displaying recipe ingredients.

        Sets up the ingredients treeview with sortable columns and populates it
        with ingredient data.
        """
        ingredients_frame = ttk.Frame(self)
        ingredients_frame.pack(fill=tk.BOTH, expand=True)

        ingredient_columns = ("Ingredient", "Quantity", "AH Single Cost", "AH Stack Cost", "Vendor Cost", "Guild Cost")
        self._ingredients_tree = TreeviewWithSort(ingredients_frame, columns=ingredient_columns, show="headings",
                                                  selectmode="browse")
        self._configure_treeview_columns(self._ingredients_tree, ingredient_columns)
        self._populate_ingredients_tree()
        self._ingredients_tree.pack(padx=10, pady=5, expand=True, fill="both")

        self._ingredients_tree.bind("<Button-1>", self._ingredients_tree.on_click)

    def _add_cost_per_synth_frame(self) -> None:
        """
        Add a frame displaying the cost per synthesis.

        Creates a frame with labels showing the total cost for one synthesis of the recipe.
        """
        cost_per_synth_frame = ttk.Frame(self)
        cost_per_synth_frame.pack()

        cost_per_synth_label = ttk.Label(cost_per_synth_frame, text="Cost / Synth:")
        cost_per_synth_label.pack(side=tk.LEFT)

        self._cost_per_synth_value_label = ttk.Label(cost_per_synth_frame)
        self._cost_per_synth_value_label.pack(side=tk.LEFT)

        if self._simulation_data.recipe.min_cost:
            value_text = f"{int(self._simulation_data.recipe.min_cost)} gil"
        else:
            value_text = "N/A"
        self._cost_per_synth_value_label.config(text=value_text)

    def _add_results_tree(self) -> None:
        """
        Create and configure the treeview for displaying recipe results.

        Sets up the results treeview with sortable columns and populates it
        with result data including prices and profits.
        """
        results_frame = ttk.Frame(self)
        results_frame.pack(fill=tk.BOTH, expand=True)

        result_columns = ("Result", "Single Price", "Stack Price", "Proportion", "Profit Contribution")
        self._results_tree = TreeviewWithSort(results_frame, columns=result_columns,
                                              show="headings", selectmode="browse")
        self._configure_treeview_columns(self._results_tree, result_columns)
        self._populate_results_tree()
        self._results_tree.pack(padx=10, pady=10, expand=True, fill="both")

        self._results_tree.bind("<Button-1>", self._results_tree.on_click)

    def _add_close_button(self) -> None:
        """
        Add a button to close the recipe detail page.

        Creates a button that, when clicked, will close the current tab and
        return to the previous tab.
        """
        close_button = ttk.Button(self, text="Close", command=self._close_detail_page)
        close_button.pack(pady=(20, 30))

    def _configure_treeview_columns(self, treeview: TreeviewWithSort, columns: list[str]) -> None:
        """
        Configure the columns for a treeview.
        Sets up the heading and column properties for each column in the treeview.

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

        Retrieves ingredient data from the recipe and inserts it into the ingredients treeview.
        """

        for ingredient, quantity in self._simulation_data.recipe.ingredients.items():
            ingredient_name = ingredient.get_formatted_sort_name()

            single_cost = int(ingredient.min_single_price * quantity) if ingredient.min_single_price else ""

            if ingredient.min_stack_price:
                single_cost_from_stack = ingredient.min_stack_price / ingredient.stack_size
                stack_cost = int(single_cost_from_stack * quantity)
                stack_cost_string = f"{int(ingredient.min_stack_price)} ({stack_cost})"
            else:
                stack_cost_string = ""

            vendor_cost = ingredient.min_vendor_cost if ingredient.min_vendor_cost is not None else ""
            guild_cost = ingredient.min_guild_cost if ingredient.min_guild_cost is not None else ""

            self._ingredients_tree.insert("", "end", iid=ingredient.item_id, values=(
                ingredient_name, quantity, single_cost, stack_cost_string, vendor_cost, guild_cost))

    def _populate_results_tree(self) -> None:
        """
        Populate the results treeview with data.

        Retrieves result data from the recipe and inserts it into the results treeview.
        """
        unique_results = self._simulation_data.recipe.get_unique_results()
        show_stack_columns = False
        for result in unique_results:
            result_name = result.get_formatted_sort_name()
            single_price = result.min_single_price if result.min_single_price is not None else ""
            stack_price = result.min_stack_price if result.min_stack_price is not None else ""
            proportion = self._simulation_data.proportions[result]
            proportion_string = f"{proportion:.2%}" if proportion is not None else ""
            profit_contribution = self._simulation_data.profit_contributions[result]
            contribution_string = f"{profit_contribution:.2%}" if profit_contribution is not None else ""

            if stack_price:
                show_stack_columns = True

            self._results_tree.insert("", "end", iid=result.item_id, values=(result_name, single_price, stack_price,
                                                                             proportion_string, contribution_string))

        self._update_results_tree_columns(show_stack_columns)

    def _update_results_tree_columns(self, show_stack_columns: bool) -> None:
        """
        Update the visibility of stack-related columns in the results tree.

        Args:
            show_stack_columns (bool): Whether to show or hide stack-related columns.
        """
        if show_stack_columns:
            self._results_tree.show_column("Stack Price")
        else:
            self._results_tree.hide_column("Stack Price")

    def _close_detail_page(self) -> None:
        """
        Close the recipe detail page.

        Removes the current tab from the notebook and returns to the previous tab.
        """
        tab_id = self._parent.notebook.index(self)
        self._parent.notebook.forget(tab_id)
        self._parent.notebook.select(self._previous_tab_index)
