import tkinter as tk
from tkinter import ttk
from views.search_page import SearchPage
from views.profit_page import ProfitPage
from views.simulate_page import SimulatePage
from views.settings_page import SettingsPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FFXI Crafting Tool")
        self.geometry("1600x900")

        self.configure_styles()
        self.create_main_frame()
        self.create_notebook()
        self.create_pages()

    def configure_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 14), padding=5)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10), padding=4)
        self.style.configure("Treeview", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("Custom.TCheckbutton", font=("Helvetica", 14))

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both")

    def create_pages(self):
        SearchPage(self)
        ProfitPage(self)
        SimulatePage(self)
        SettingsPage(self)


if __name__ == "__main__":
    app = App()
    app.mainloop()
