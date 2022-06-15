class Product:
    def __init__(self, item_name, quantity, sell_price, sell_frequency,
                 cost) -> None:
        self.item_name = item_name
        self.quantity = quantity
        self.sell_price = sell_price
        self.sell_frequency = sell_frequency
        self.cost = cost
        self.profit = sell_price - cost
        self.value = (self.profit * sell_frequency) / 1000

    @staticmethod
    def filter_products(products, profit_threshold, freq_threshold,
                        value_threshold):
        """Removes duplicates from different recipes that are less profitable
        and any that don't pass thresholds
        """
        filtered = []
        for product in products:
            duplicate = any(x.item_name == product.item_name and
                            x.quantity == product.quantity for x in filtered)
            profitable = product.profit >= profit_threshold
            fast_selling = product.sell_frequency >= freq_threshold
            valuable = product.value >= value_threshold

            if profitable and fast_selling and valuable and not duplicate:
                filtered.append(product)

        return filtered
