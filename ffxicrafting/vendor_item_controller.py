from database import Database
from vendor_item import VendorItem


class VendorItemController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_vendor_item(cls, item_name, vendor_name):
        vendor_item_tuple = cls.db.get_vendor_item(item_name, vendor_name)
        if vendor_item_tuple is not None:
            return VendorItem(*vendor_item_tuple)
        else:
            return None

    @classmethod
    def add_vendor_item(cls, item_name, vendor_name, price):
        vendor_item = VendorItem(item_name, vendor_name, price)
        cls.db.add_vendor_item(vendor_item)

    @classmethod
    def remove_vendor_item(cls, item_name, vendor_name):
        cls.db.remove_vendor_item(item_name, vendor_name)
