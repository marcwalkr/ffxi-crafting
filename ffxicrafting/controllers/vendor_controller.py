from database import Database
from models.vendor_item import VendorItem


class VendorController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_vendor_items(cls, item_id):
        vendor_item_tuples = cls.db.get_vendor_items(item_id)

        vendor_items = []
        for vendor_item_tuple in vendor_item_tuples:
            vendor_item = VendorItem(*vendor_item_tuple)
            vendor_items.append(vendor_item)

        return vendor_items
