from database import Database
from vendor import Vendor


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
