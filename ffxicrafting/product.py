from database import Database


class Product:
    db = Database()

    def __init__(self, name, quantity, cost, sell_price,
                 sell_freq) -> None:
        self.name = name
        self.quantity = quantity
        self.cost = cost
        self.sell_price = sell_price
        self.sell_freq = sell_freq
        self.profit = sell_price - cost

    @classmethod
    def get_products(cls, profit_threshold, freq_threshold):
        all_recipes = cls.db.get_all_recipes()

        products = []

        for recipe in all_recipes:
            crafted_products = cls.get_crafted_products(recipe)
            products += crafted_products

        products = cls.filter_threshold(products, profit_threshold,
                                        freq_threshold)
        profit_sorted = sorted(products, key=lambda x: x.profit, reverse=True)

        return profit_sorted

    @classmethod
    def get_crafted_products(cls, recipe):
        products = []

        recipe_name = recipe[0]
        auction_listings = cls.db.get_auction_listings(recipe_name)

        for listing in auction_listings:
            name, quantity, sell_price, sell_freq = listing
            synth_yield = recipe[10]
            synth_cost = recipe[16]
            product_cost = (synth_cost / synth_yield) * quantity

            product = cls(name, quantity, product_cost, sell_price, sell_freq)
            products.append(product)

        return products

    @staticmethod
    def filter_threshold(products, profit_threshold, freq_threshold):
        filtered = []
        for product in products:
            profitable = product.profit >= profit_threshold
            fast_selling = product.sell_freq >= freq_threshold

            if profitable and fast_selling:
                filtered.append(product)

        return filtered
