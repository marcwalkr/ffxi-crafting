from database import Database


class VendorItem:
    db = Database()

    def __init__(self, item_name, vendor_name, price) -> None:
        self.item_name = item_name
        self.vendor_name = vendor_name
        self.price = price

    def to_database(self):
        self.db.add_vendor_item(self)

    @classmethod
    def remove_vendor_item(cls, item_name, vendor_name):
        cls.db.remove_vendor_item(item_name, vendor_name)

    @classmethod
    def is_in_database(cls, item_name, vendor_name):
        return cls.db.vendor_item_is_in_database(item_name, vendor_name)
