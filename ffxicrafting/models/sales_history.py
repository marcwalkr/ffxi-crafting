class SalesHistory:
    def __init__(self, id, item_id, sell_date, buyer, seller, price, batch_id, is_stack):
        self.id = id
        self.item_id = item_id
        self.sell_date = sell_date
        self.buyer = buyer
        self.seller = seller
        self.price = price
        self.batch_id = batch_id
        self.is_stack = is_stack
