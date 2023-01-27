from database import Database
from models.vendor_item import VendorItem
from models.regional_vendor import RegionalVendor
from config import Config


class VendorController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_vendor_items(cls, item_id):
        ignored_regions = Config.get_ignored_regions()
        regional_vendors = cls.get_regional_vendors()

        ignored_npc_ids = []
        for vendor in regional_vendors:
            if vendor.region in ignored_regions:
                ignored_npc_ids.append(vendor.npc_id)

        vendor_item_tuples = cls.db.get_vendor_items(item_id)

        vendor_items = []
        for vendor_item_tuple in vendor_item_tuples:
            vendor_item = VendorItem(*vendor_item_tuple)
            if vendor_item.npc_id not in ignored_npc_ids:
                vendor_items.append(vendor_item)

        return vendor_items

    @classmethod
    def get_regional_vendors(cls):
        regional_vendor_tuples = cls.db.get_regional_vendors()
        return [RegionalVendor(*r) for r in regional_vendor_tuples]
