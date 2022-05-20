from database import Database
from helpers import sort_alphabetically


class Item:
    db = Database()

    def __init__(self, name, stackable, stack_quantity, craftable,
                 vendor_location, vendor_price) -> None:
        self.name = name
        self.stackable = stackable
        self.stack_quantity = stack_quantity
        self.craftable = craftable
        self.vendor_location = vendor_location
        self.vendor_price = vendor_price

    def add_to_database(self):
        self.db.add_item(self)

    @classmethod
    def get_all_items(cls):
        all_items = []
        all_item_tuples = cls.db.get_all_items()
        for item_tuple in all_item_tuples:
            item = cls(*item_tuple)
            all_items.append(item)

        sorted = sort_alphabetically(all_items)

        return sorted

    @classmethod
    def remove_item(cls, item_name):
        cls.db.remove_item(item_name)

    @classmethod
    def update_vendor_price(cls, item_name, new_price):
        cls.db.update_item_vendor_price(item_name, new_price)

    @classmethod
    def update_vendor_location(cls, item_name, new_location):
        cls.db.update_item_vendor_location(item_name, new_location)

    @classmethod
    def is_in_database(cls, name):
        return cls.db.item_is_in_database(name)
