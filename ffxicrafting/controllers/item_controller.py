from functools import lru_cache
from database.database import Database
from entities.item import Item


class ItemController:
    db = Database()

    def __init__(self) -> None:
        pass

    @classmethod
    @lru_cache(maxsize=None)
    def get_item(cls, item_id):
        item_tuple = cls.db.get_item(item_id)

        if item_tuple is not None:
            return Item(*item_tuple)
        else:
            return None
