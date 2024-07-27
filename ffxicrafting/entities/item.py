from models import ItemModel


class Item(ItemModel):
    def __init__(self, item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell) -> None:
        super().__init__(item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell)
        self.item_id = item_id
        self.single_price = None
        self.stack_price = None
        self.single_sell_freq = None
        self.stack_sell_freq = None

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Item):
            return self.item_id == __value.item_id
        return False

    def __hash__(self) -> int:
        return hash(self.item_id)

    def get_formatted_name(self):
        return self.sort_name.replace("_", " ").title()

    def update_from_item(self, item):
        self.single_price = item.single_price
        self.stack_price = item.stack_price
        self.single_sell_freq = item.single_sell_freq
        self.stack_sell_freq = item.stack_sell_freq


class CraftableItem(Item):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.crafted_cost = None
