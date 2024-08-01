from entities import CraftableItem


class Result(CraftableItem):
    instances = []

    def __init__(self, item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell):
        super().__init__(item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell)
        self.single_profit = None
        self.stack_profit = None
        Result.instances.append(self)

    @classmethod
    def get(cls, item_id):
        for result in cls.instances:
            if result.item_id == item_id:
                return result
        return None

    @classmethod
    def sync(cls, item):
        for result in cls.instances:
            if result.item_id == item.item_id:
                result.update_from_item(item)
