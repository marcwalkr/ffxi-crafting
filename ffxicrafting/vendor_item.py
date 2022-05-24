from database import Database
from text_ui import TextUI


class VendorItem:
    db = Database()

    def __init__(self, item_name, vendor_name, price) -> None:
        self.item_name = item_name
        self.vendor_name = vendor_name
        self.price = price

    def to_database(self):
        self.db.add_vendor_item(self)

    @classmethod
    def prompt_add_vendor_item(cls):
        item_name = TextUI.prompt_item_name()
        vendor_name = TextUI.prompt_vendor_name()
        price = TextUI.prompt_vendor_price()

        vendor_item = cls(item_name, vendor_name, price)
        vendor_item.to_database()

    @classmethod
    def prompt_remove_vendor_item(cls):
        item_name = TextUI.prompt_item_name()
        vendor_name = TextUI.prompt_vendor_name()

        if cls.is_in_database(item_name, vendor_name):
            cls.remove_vendor_item(item_name, vendor_name)
        else:
            TextUI.print_error_vendor_item_not_in_db(item_name, vendor_name)

    @classmethod
    def remove_vendor_item(cls, item_name, vendor_name):
        cls.db.remove_vendor_item(item_name, vendor_name)

    @classmethod
    def is_in_database(cls, item_name, vendor_name):
        return cls.db.vendor_item_is_in_database(item_name, vendor_name)
