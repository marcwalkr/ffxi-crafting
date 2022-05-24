from database import Database
from text_ui import TextUI


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
    def prompt_add_vendor(cls):
        npc_name, area, coordinates, vendor_type = TextUI.prompt_vendor()
        vendor = cls(npc_name, area, coordinates, vendor_type)
        vendor.to_database()

    @classmethod
    def prompt_remove_vendor(cls):
        npc_name = TextUI.prompt_vendor_name()

        if cls.is_in_database(npc_name):
            cls.remove_vendor(npc_name)
        else:
            TextUI.print_error_vendor_not_in_db(npc_name)

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
