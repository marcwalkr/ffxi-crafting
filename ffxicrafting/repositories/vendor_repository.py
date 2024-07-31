from models import VendorItem, RegionalVendor, VendorLocation
from functools import lru_cache


class VendorRepository:
    def __init__(self, db) -> None:
        self.db = db

    @lru_cache(maxsize=None)
    def get_vendor_items(self, item_id):
        vendor_item_tuples = self.db.get_vendor_items(item_id)
        if vendor_item_tuples:
            return [VendorItem(*v) for v in vendor_item_tuples]
        else:
            return []

    @lru_cache(maxsize=None)
    def get_regional_vendor(self, npc_id):
        regional_vendor_tuple = self.db.get_regional_vendor(npc_id)
        if regional_vendor_tuple:
            return RegionalVendor(*regional_vendor_tuple)
        else:
            return None

    @lru_cache(maxsize=None)
    def get_vendor_location(self, npc_id):
        vendor_location_tuple = self.db.get_vendor_location(npc_id)
        if vendor_location_tuple:
            return VendorLocation(*vendor_location_tuple)
        else:
            return None
