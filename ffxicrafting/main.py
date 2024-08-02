import tkinter as tk
import logging
from tkinter import ttk
from views import SearchPage, ProfitPage, SettingsPage, RecipeListPage

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


class App(tk.Tk):
    """
    Main application class for the FFXI Crafting Tool.

    This class sets up the main window, configures styles, and manages the different pages
    of the application using a notebook interface.
    """

    def __init__(self):
        """Initialize the main application window and set up its components."""
        super().__init__()
        self.title("FFXI Crafting Tool")
        self.geometry("1600x900")

        self.recipe_pages = []

        self.configure_styles()
        self.create_main_frame()
        self.create_notebook()
        self.create_pages()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def configure_styles(self):
        """Configure the styles for various UI elements."""
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 14), padding=5)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10), padding=4)
        self.style.configure("Treeview", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("Custom.TCheckbutton", font=("Helvetica", 14))
        self.style.configure("TMenubutton", font=("Helvetica", 12))

    def create_main_frame(self):
        """Create and set up the main frame of the application."""
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

    def create_notebook(self):
        """Create the notebook widget to hold different pages."""
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both")

    def create_pages(self):
        """Create and initialize the different pages of the application."""
        self.pages = [
            SearchPage(self),
            ProfitPage(self),
            SettingsPage(self)
        ]
        for page in self.pages:
            if isinstance(page, RecipeListPage):
                self.recipe_pages.append(page)

    def on_close(self):
        """Handle the application closing event."""
        self.cleanup_pages()
        self.destroy()

    def cleanup_pages(self):
        """Clean up resources used by recipe pages before closing."""
        for page in self.recipe_pages:
            page.cleanup()
        self.recipe_pages.clear()


def main():
    """
    Main function to run the FFXI Crafting Tool application.

    This function creates an instance of the App class and starts the main event loop.
    """
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
