from database import Database
from helpers import sort_alphabetically


class Item:
    db = Database()

    def __init__(self, name, stack_quantity, vendor_price) -> None:
        self.name = name
        self.stack_quantity = stack_quantity
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
    def get_item(cls, name):
        item_tuple = cls.db.get_item(name)
        if item_tuple is not None:
            item = cls(*item_tuple)
            return item
        else:
            return None

    @classmethod
    def remove_item(cls, item_name):
        cls.db.remove_item(item_name)

    @classmethod
    def update_vendor_price(cls, item_name, new_price):
        cls.db.update_item_vendor_price(item_name, new_price)

    @classmethod
    def is_in_database(cls, name):
        return cls.db.item_is_in_database(name)
