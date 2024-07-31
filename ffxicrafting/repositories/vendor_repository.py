from models import VendorItem, RegionalVendor, VendorLocation


class VendorRepository:
    vendor_item_cache = {}
    regional_vendor_cache = {}
    vendor_location_cache = {}

    def __init__(self, db) -> None:
        self.db = db

    def get_vendor_items(self, item_id):
        if item_id in self.vendor_item_cache:
            return self.vendor_item_cache[item_id]
        else:
            vendor_item_tuples = self.db.get_vendor_items(item_id)
            if vendor_item_tuples:
                self.vendor_item_cache[item_id] = [VendorItem(*v) for v in vendor_item_tuples]
                return self.vendor_item_cache[item_id]

            self.vendor_item_cache[item_id] = []
            return []

    def get_regional_vendor(self, npc_id):
        if npc_id in self.regional_vendor_cache:
            return self.regional_vendor_cache[npc_id]
        else:
            regional_vendor_tuple = self.db.get_regional_vendor(npc_id)
            if regional_vendor_tuple:
                self.regional_vendor_cache[npc_id] = RegionalVendor(*regional_vendor_tuple)
                return self.regional_vendor_cache[npc_id]
            return None

    def get_vendor_location(self, npc_id):
        if npc_id in self.vendor_location_cache:
            return self.vendor_location_cache[npc_id]
        else:
            vendor_location_tuple = self.db.get_vendor_location(npc_id)
            if vendor_location_tuple:
                self.vendor_location_cache[npc_id] = VendorLocation(*vendor_location_tuple)
                return self.vendor_location_cache[npc_id]
            return None
