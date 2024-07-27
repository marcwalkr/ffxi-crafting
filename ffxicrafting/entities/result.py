from entities import CraftableItem


class Result(CraftableItem):
    instances = []

    def __init__(self, item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell):
        super().__init__(item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell)
        self.single_profit = None
        self.stack_profit = None
        Result.instances.append(self)
