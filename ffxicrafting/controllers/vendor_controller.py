from database.database import Database
from models.vendor_item import VendorItem
from models.regional_vendor import RegionalVendor


class VendorController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_vendor_items(cls, item_id):
        vendor_item_tuples = cls.db.get_vendor_items(item_id)
        return [VendorItem(*v) for v in vendor_item_tuples]

    @classmethod
    def get_regional_vendors(cls):
        regional_vendor_tuples = cls.db.get_regional_vendors()
        return [RegionalVendor(*r) for r in regional_vendor_tuples]
