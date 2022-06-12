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

    @classmethod
    def add_item_cost(cls, item_id, source_id, cost):
        cls.db.add_item_cost(item_id, source_id, cost)

    @classmethod
    def update_item_cost(cls, item_id, source_id, cost):
        cls.db.update_item_cost(item_id, source_id, cost)
