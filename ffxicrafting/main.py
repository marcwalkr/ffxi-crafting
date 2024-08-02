import tkinter as tk
import logging
from tkinter import ttk
from views import SearchPage, ProfitPage, SettingsPage, RecipeListPage

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class App(tk.Tk):
    """
    Main application class for the FFXI Crafting Tool.

    This class sets up the main window, configures styles, and manages the different pages
    of the application using a notebook interface. It handles the creation and cleanup of
    pages, as well as the overall application lifecycle.
    """

    def __init__(self) -> None:
        """
        Initialize the main application window and set up its components.

        Creates the main frame, configures styles, sets up the notebook, and initializes
        the application pages. Also sets up the window close protocol.
        """
        super().__init__()
        self.title("FFXI Crafting Tool")
        self.geometry("1600x900")

        self._recipe_pages: list[RecipeListPage] = []

        self._main_frame: ttk.Frame = None
        self.notebook: ttk.Notebook = None

        self._configure_styles()
        self._create_main_frame()
        self._create_notebook()
        self._create_pages()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def _configure_styles(self) -> None:
        """
        Configure the styles for various UI elements.

        Sets up custom styles for buttons, labels, notebook tabs, treeviews,
        checkbuttons, and menubuttons to ensure a consistent look across the application.
        """
        style = ttk.Style(self)
        style.configure("TButton", font=("Helvetica", 14), padding=10)
        style.configure("TLabel", font=("Helvetica", 14), padding=5)
        style.configure("TNotebook.Tab", font=("Helvetica", 10), padding=4)
        style.configure("Treeview", font=("Helvetica", 12))
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        style.configure("Custom.TCheckbutton", font=("Helvetica", 14))
        style.configure("TMenubutton", font=("Helvetica", 12))

    def _create_main_frame(self) -> None:
        """
        Create and set up the main frame of the application.

        Initializes the main frame and packs it to fill the entire window.
        """
        self._main_frame = ttk.Frame(self)
        self._main_frame.pack(expand=True, fill="both")

    def _create_notebook(self) -> None:
        """
        Create the notebook widget to hold different pages.

        Initializes the notebook and packs it to fill the main frame.
        """
        self.notebook = ttk.Notebook(self._main_frame)
        self.notebook.pack(expand=True, fill="both")

    def _create_pages(self) -> None:
        """
        Create and initialize the different pages of the application.

        Instantiates SearchPage, ProfitPage, and SettingsPage. Adds RecipeListPages
        to the _recipe_pages list for later cleanup.
        """
        pages = [
            SearchPage(self),
            ProfitPage(self),
            SettingsPage(self)
        ]
        for page in pages:
            if isinstance(page, RecipeListPage):
                self._recipe_pages.append(page)

    def on_close(self) -> None:
        """
        Handle the application closing event.

        Performs cleanup operations on pages and destroys the main window.
        """
        self._cleanup_pages()
        self.destroy()

    def _cleanup_pages(self) -> None:
        """
        Clean up resources used by recipe pages before closing.

        Calls the cleanup method on each RecipeListPage and clears the list.
        """
        for page in self._recipe_pages:
            page.cleanup()
        self._recipe_pages.clear()


def main() -> None:
    """
    Main function to run the FFXI Crafting Tool application.

    Creates an instance of the App class and starts the main event loop.
    This function serves as the entry point for the application.
    """
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
