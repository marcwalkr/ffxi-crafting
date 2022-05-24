from database import Database


class Item:
    db = Database()

    def __init__(self, name, full_name, stack_quantity) -> None:
        self.name = name
        self.full_name = full_name
        self.stack_quantity = stack_quantity

    def to_database(self):
        self.db.add_item(self)

    @classmethod
    def get_item(cls, name):
        item_tuple = cls.db.get_item(name)
        if item_tuple is not None:
            item = cls(*item_tuple)
            return item
        else:
            return None

    # @classmethod
    # def get_all_items(cls):
    #     all_items = []
    #     all_item_tuples = cls.db.get_all_items()
    #     for item_tuple in all_item_tuples:
    #         item = cls(*item_tuple)
    #         all_items.append(item)

    #     return all_items

    @classmethod
    def remove_item(cls, item_name):
        cls.db.remove_item(item_name)

    @classmethod
    def is_in_database(cls, name):
        return cls.db.item_is_in_database(name)
