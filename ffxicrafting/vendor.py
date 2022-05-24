from database import Database


class Vendor:
    db = Database()

    def __init__(self, npc_name, area, coordinates, vendor_type) -> None:
        self.npc_name = npc_name
        self.area = area
        self.coordinates = coordinates
        self.vendor_type = vendor_type

    def to_database(self):
        self.db.add_vendor(self)

    @classmethod
    def get_vendor(cls, npc_name):
        vendor_tuple = cls.db.get_vendor(npc_name)
        if vendor_tuple is not None:
            vendor = cls(*vendor_tuple)
            return vendor
        else:
            return None

    @classmethod
    def remove_vendor(cls, npc_name):
        cls.db.remove_vendor(npc_name)

    @classmethod
    def is_in_database(cls, npc_name):
        return cls.db.vendor_is_in_database(npc_name)
