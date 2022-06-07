class Product:
    def __init__(self, item_name, quantity, sell_price, sell_frequency,
                 cost) -> None:
        self.item_name = item_name
        self.quantity = quantity
        self.sell_price = sell_price
        self.sell_frequency = sell_frequency
        self.cost = cost
        self.profit = sell_price - cost
        self.value = self.profit * sell_frequency

    @classmethod
    def get_products(cls, profit_threshold, freq_threshold):
        pass
