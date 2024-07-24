from entities.item import Item


class Result(Item):
    instances = []

    def __init__(self, item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell):
        super().__init__(item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell)
        self.crafted_cost = None
        self.single_profit = None
        self.stack_profit = None
        Result.instances.append(self)

    def update_from_item(self, item):
        self.single_price = item.single_price
        self.stack_price = item.stack_price
        self.single_sell_freq = item.single_sell_freq
        self.stack_sell_freq = item.stack_sell_freq
