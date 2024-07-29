import tkinter as tk
from tkinter import ttk
from views import SearchPage, ProfitPage, SettingsPage
from database import Database
import threading


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FFXI Crafting Tool")
        self.geometry("1600x900")

        self.configure_styles()
        self.create_main_frame()
        self.create_notebook()
        self.create_pages()

        threading.Thread(target=Database.initialize_pool, daemon=True).start()

    def configure_styles(self):
        self.style = ttk.Style(self)
        self.style.configure("TButton", font=("Helvetica", 14), padding=10)
        self.style.configure("TLabel", font=("Helvetica", 14), padding=5)
        self.style.configure("TNotebook.Tab", font=("Helvetica", 10), padding=4)
        self.style.configure("Treeview", font=("Helvetica", 12))
        self.style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"))
        self.style.configure("Custom.TCheckbutton", font=("Helvetica", 14))
        self.style.configure("TMenubutton", font=("Helvetica", 12))

    def create_main_frame(self):
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(expand=True, fill="both")

    def create_notebook(self):
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both")

    def create_pages(self):
        SearchPage(self)
        ProfitPage(self)
        SettingsPage(self)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
