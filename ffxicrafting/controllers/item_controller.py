from database.database import Database
from entities.item import Item


class ItemController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    def get_item(cls, item_id):
        item_tuple = cls.db.get_item(item_id)

        if item_tuple is not None:
            return Item(*item_tuple)
        else:
            return None

    @classmethod
    def get_item_by_name(cls, item_name):
        item_tuple = cls.db.get_item_by_name(item_name)

        if item_tuple is not None:
            return Item(*item_tuple)
        else:
            return None

    @classmethod
    def get_formatted_item_name(cls, item_id):
        item = cls.get_item(item_id)
        if item:
            return item.get_formatted_name()
        return None
