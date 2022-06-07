from database import Database
from models.item import Item


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
