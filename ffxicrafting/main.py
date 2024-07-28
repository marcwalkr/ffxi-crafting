import tkinter as tk
from tkinter import ttk
from views import SearchPage, ProfitPage, SettingsPage
from database import Database
from repositories import AuctionRepository, VendorRepository, GuildRepository
from services import ItemService, AuctionService, RecipeService, CraftingService


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.setup_services()

        self.title("FFXI Crafting Tool")
        self.geometry("1600x900")

        self.configure_styles()
        self.create_main_frame()
        self.create_notebook()
        self.create_pages()

    def setup_services(self):
        auction_repository = AuctionRepository(self.db)
        vendor_repository = VendorRepository(self.db)
        guild_repository = GuildRepository(self.db)
        auction_service = AuctionService(auction_repository)
        item_service = ItemService(self.db, auction_service, vendor_repository, guild_repository)
        self.recipe_service = RecipeService(self.db, item_service)
        self.crafting_service = CraftingService(item_service)

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
        SearchPage(self, self.recipe_service, self.crafting_service)
        ProfitPage(self, self.recipe_service, self.crafting_service)
        SettingsPage(self)


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
