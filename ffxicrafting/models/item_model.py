class ItemModel:
    def __init__(self, item_id, sub_id, name, sort_name, stack_size, flags, ah,
                 no_sale, base_sell) -> None:
        self.item_id = item_id
        self.sub_id = sub_id
        self.name = name
        self.sort_name = sort_name
        self.stack_size = stack_size
        self.flags = flags
        self.ah = ah
        self.no_sale = no_sale
        self.base_sell = base_sell
