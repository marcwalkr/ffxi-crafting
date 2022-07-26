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
        profit_sorted = sorted(products, key=lambda x: x.profit, reverse=True)
        filtered = []
        for product in profit_sorted:
            duplicate = any(x.item_name == product.item_name and
                            x.quantity == product.quantity for x in filtered)
            profitable = product.profit >= profit_threshold
            fast_selling = product.sell_frequency >= freq_threshold
            valuable = product.value >= value_threshold

            if profitable and fast_selling and valuable and not duplicate:
                filtered.append(product)

        return filtered

    @staticmethod
    def sort_products(products, sort_method):
        if sort_method == "item_name":
            sorted_products = sorted(products, key=lambda x: x.item_name)
        elif sort_method == "cost":
            sorted_products = sorted(products, key=lambda x: x.cost)
        elif sort_method == "profit":
            sorted_products = sorted(products, key=lambda x: x.profit,
                                     reverse=True)
        elif sort_method == "sell_frequency":
            sorted_products = sorted(products, key=lambda x: x.sell_frequency,
                                     reverse=True)
        else:
            sorted_products = sorted(products, key=lambda x: x.value,
                                     reverse=True)

        return sorted_products
