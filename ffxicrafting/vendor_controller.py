from database import Database
from vendor import Vendor
from vendor_item import VendorItem


class VendorController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_vendor(cls, npc_name):
        vendor_tuple = cls.db.get_vendor(npc_name)
        if vendor_tuple is not None:
            return Vendor(*vendor_tuple)
        else:
            return None

    @classmethod
    def add_vendor(cls, npc_name, area, coordinates, vendor_type):
        vendor = Vendor(npc_name, area, coordinates, vendor_type)
        cls.db.add_vendor(vendor)

    @classmethod
    def remove_vendor(cls, npc_name):
        cls.db.remove_vendor(npc_name)

    @classmethod
    def vendor_exists(cls, npc_name):
        return cls.get_vendor(npc_name) is not None

    @classmethod
    def get_vendor_item(cls, item_name, vendor_name):
        vendor_item_tuple = cls.db.get_vendor_item(item_name, vendor_name)
        if vendor_item_tuple is not None:
            return VendorItem(*vendor_item_tuple)
        else:
            return None

    @classmethod
    def get_vendor_items(cls, item_name):
        vendor_items = []

        vendor_item_tuples = cls.db.get_vendor_items_by_item(item_name)
        for vendor_item_tuple in vendor_item_tuples:
            vendor_item = VendorItem(*vendor_item_tuple)
            vendor_items.append(vendor_item)

        return vendor_items

    @classmethod
    def add_vendor_item(cls, item_name, vendor_name, price):
        vendor_item = VendorItem(item_name, vendor_name, price)
        cls.db.add_vendor_item(vendor_item)

    @classmethod
    def remove_vendor_item(cls, item_name, vendor_name):
        cls.db.remove_vendor_item(item_name, vendor_name)

    @classmethod
    def update_vendor_price(cls, item_name, vendor_name, price):
        cls.db.update_vendor_price(item_name, vendor_name, price)

    @classmethod
    def vendor_item_exists(cls, item_name, vendor_name):
        return cls.get_vendor_item(item_name, vendor_name) is not None
