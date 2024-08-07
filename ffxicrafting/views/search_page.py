import tkinter as tk
from tkinter import ttk
from controllers import RecipeController
from entities import Recipe
from views import RecipeListPage


class SearchPage(RecipeListPage):
    """
    A page for searching for FFXI crafting recipes.

    This class extends RecipeListPage to provide functionality specific to searching for crafting recipes,
    including custom treeview columns and formatted display of search results.
    """

    def __init__(self, parent: tk.Tk) -> None:
        """
        Initialize the search page.
        Initializes search-specific attributes and calls the parent constructor.

        Args:
            parent (tk.Tk): The parent Tkinter application.
        """
        self.action_button_text = "Search"
        self._search_var: tk.StringVar = None
        self._search_entry: ttk.Entry = None
        super().__init__(parent)

    def get_tab_text(self) -> str:
        """
        Return the text for the tab.

        Returns:
            str: The text "Search Recipes" to be displayed on the tab.
        """
        return "Search Recipes"

    def create_action_frame(self) -> None:
        """
        Create the search input and button within the action frame.
        """
        super().create_action_frame()

        self._search_var = tk.StringVar()

        self._search_entry = ttk.Entry(self.action_frame, textvariable=self._search_var,
                                       font=("Helvetica", 14), width=20)
        self._search_entry.pack(side=tk.LEFT, padx=(0, 10))
        self._search_entry.bind("<Return>", lambda event: self.start_process())

        # Move the action button to the right of the entry
        if hasattr(self, 'action_button'):
            self.action_button.pack_forget()  # Unpack from its current position
            self.action_button.pack(side=tk.RIGHT)  # Pack to the right

    def get_treeview_columns(self) -> list[str]:
        """
        Return the columns for the treeview.

        Returns:
            list[str]: A list of column identifiers for the treeview:
            ["nq", "hq", "levels", "ingredients"]
        """
        return ("nq", "hq", "levels", "ingredients")

    def configure_treeview(self, treeview: ttk.Treeview) -> None:
        """
        Configure the treeview settings.
        Sets up column headings, text, and alignment for the search results treeview.

        Args:
            treeview (ttk.Treeview): The treeview to configure.
        """
        treeview.heading("nq", text="NQ")
        treeview.heading("hq", text="HQ")
        treeview.heading("levels", text="Craft Levels")
        treeview.heading("ingredients", text="Ingredients")
        treeview.column("levels", anchor=tk.CENTER)

    def get_recipe_batch(self, recipe_controller: RecipeController, batch_size: int, offset: int) -> list[Recipe]:
        """
        Fetch a batch of recipes based on the user's search query.

        Args:
            recipe_controller (RecipeController): The recipe controller to use.
            batch_size (int): The number of recipes to fetch.
            offset (int): The offset for pagination.

        Returns:
            list: A list of Recipe objects matching the search query,
                  fetched from RecipeController.
        """
        return recipe_controller.search_recipe(self._search_var.get(), batch_size, offset)

    def format_row(self, craft_result: dict[str, any]) -> list[str]:
        """
        Format a row for the treeview based on the craft result.

        Args:
            craft_result (dict[str, any]): The craft result to format.

        Returns:
            list[str]: A list of formatted strings for the treeview:
            [0] NQ result: Formatted string of the normal quality result
            [1] HQ results: Formatted string of the high quality results
            [2] Craft levels: Formatted string of the required crafting levels
            [3] Ingredients: Formatted string of the required ingredients
        """
        recipe = craft_result["crafter"].recipe

        return [
            recipe.get_formatted_nq_result(),
            recipe.get_formatted_hq_results(),
            recipe.get_formatted_levels_string(),
            recipe.get_formatted_ingredient_names()
        ]
