from database import Database
from item import Item


class ItemController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_item(cls, name):
        item_tuple = cls.db.get_item(name)
        if item_tuple is not None:
            return Item(*item_tuple)
        else:
            return None

    @classmethod
    def get_all_items(cls):
        all_items = []
        all_item_tuples = cls.db.get_all_items()
        for item_tuple in all_item_tuples:
            item = Item(*item_tuple)
            all_items.append(item)

        return all_items

    @classmethod
    def add_item(cls, item_name, stack_quantity):
        item = Item(item_name, stack_quantity)
        cls.db.add_item(item)

    @classmethod
    def remove_item(cls, item_name):
        cls.db.remove_item(item_name)
