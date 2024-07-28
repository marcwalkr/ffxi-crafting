from models import VendorItem, RegionalVendor, VendorLocation


class VendorRepository:
    def __init__(self, db) -> None:
        self.db = db
        self.cache = {
            "get_vendor_items": {},
            "get_regional_vendor": {},
            "get_vendor_location": {}
        }

    def get_vendor_items(self, item_id):
        if item_id in self.cache["get_vendor_items"]:
            return self.cache["get_vendor_items"][item_id]
        else:
            vendor_item_tuples = self.db.get_vendor_items(item_id)
            if vendor_item_tuples:
                self.cache["get_vendor_items"][item_id] = [VendorItem(*v) for v in vendor_item_tuples]
                return self.cache["get_vendor_items"][item_id]

            self.cache["get_vendor_items"][item_id] = []
            return []

    def get_regional_vendor(self, npc_id):
        if npc_id in self.cache["get_regional_vendor"]:
            return self.cache["get_regional_vendor"][npc_id]
        else:
            regional_vendor_tuple = self.db.get_regional_vendor(npc_id)
            if regional_vendor_tuple:
                self.cache["get_regional_vendor"][npc_id] = RegionalVendor(*regional_vendor_tuple)
                return self.cache["get_regional_vendor"][npc_id]
            return None

    def get_vendor_location(self, npc_id):
        if npc_id in self.cache["get_vendor_location"]:
            return self.cache["get_vendor_location"][npc_id]
        else:
            vendor_location_tuple = self.db.get_vendor_location(npc_id)
            if vendor_location_tuple:
                self.cache["get_vendor_location"][npc_id] = VendorLocation(*vendor_location_tuple)
                return self.cache["get_vendor_location"][npc_id]
            return None
