from models import VendorItem, RegionalVendor


class VendorController:
    _cache = {
        "get_vendor_items": {},
        "get_regional_vendors": []
    }

    def __init__(self, db) -> None:
        self.db = db

    def get_vendor_items(self, item_id):
        if item_id in self._cache["get_vendor_items"]:
            return self._cache["get_vendor_items"][item_id]
        else:
            vendor_item_tuples = self.db.get_vendor_items(item_id)
            if vendor_item_tuples:
                self._cache["get_vendor_items"][item_id] = [VendorItem(*v) for v in vendor_item_tuples]
                return self._cache["get_vendor_items"][item_id]

            self._cache["get_vendor_items"][item_id] = []
            return []

    def get_regional_vendors(self):
        if self._cache["get_regional_vendors"]:
            return self._cache["get_regional_vendors"]
        else:
            regional_vendor_tuples = self.db.get_regional_vendors()
            if regional_vendor_tuples:
                self._cache["get_regional_vendors"] = [RegionalVendor(*r) for r in regional_vendor_tuples]
                return self._cache["get_regional_vendors"]
            return []
