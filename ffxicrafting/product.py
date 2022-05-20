from database import Database


class Product:
    db = Database()

    def __init__(self, name, quantity, crafted, cost, sell_price,
                 sell_freq) -> None:
        self.name = name
        self.quantity = quantity
        self.crafted = crafted
        self.cost = cost
        self.sell_price = sell_price
        self.sell_freq = sell_freq
        self.profit = sell_price - cost

    @classmethod
    def get_products(cls, profit_threshold, freq_threshold):
        all_items = cls.db.get_all_items()
        all_recipes = cls.db.get_all_recipes()

        products = []

        # Iterate through items to get vendor products
        for item in all_items:
            item_name = item[0]
            vendor_location = item[4]
            if vendor_location is None:
                continue

            # Get every auction listing for the item (single, stack)
            listings = cls.db.get_auction_listings(item_name)
            vendor_products = cls.get_vendor_products(item, listings)
            products += vendor_products

        # Iterate through recipes to get crafted products
        for recipe in all_recipes:
            # Get every auction listing for the recipe item (single, stack)
            recipe_name = recipe[0]
            listings = cls.db.get_auction_listings(recipe_name)
            crafted_products = cls.get_crafted_products(recipe, listings)
            products += crafted_products

        # Remove products that don't pass thresholds
        products = cls.filter_threshold(products, profit_threshold,
                                        freq_threshold)
        # Remove less profitable products with the same auction listing
        products = cls.remove_less_profitable_duplicates(products)

        return products

    @classmethod
    def get_vendor_products(cls, item, auction_listings):
        """Gets products that are purchased from a vendor, not crafted"""
        vendor_price = item[5]

        products = []
        for listing in auction_listings:
            name, quantity, sell_price, sell_freq = listing
            crafted = False
            cost = vendor_price * quantity

            product = cls(name, quantity, crafted, cost, sell_price, sell_freq)
            products.append(product)

        return products

    @classmethod
    def get_crafted_products(cls, recipe, auction_listings):
        """Gets products that are crafted from a recipe"""
        products = []
        for listing in auction_listings:
            name, quantity, sell_price, sell_freq = listing
            crafted = True
            synth_yield, synth_cost = recipe[10:]
            product_cost = (synth_cost / synth_yield) * quantity

            product = cls(name, quantity, crafted,
                          product_cost, sell_price, sell_freq)
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

    @staticmethod
    def remove_less_profitable_duplicates(products):
        """Removes products from a product list that have the same auction
        listing (same item and quantity) as a more profitable product
        Can happen when it's profitable to craft and less profitable to buy
        from a vendor or vice versa
        """
        profit_sorted = sorted(products, key=lambda x: x.profit, reverse=True)

        duplicates_removed = []
        for product in profit_sorted:
            # The product was already appended to list,
            # this is less profitable duplicate
            duplicate = any(x.name == product.name and
                            x.quantity == product.quantity
                            for x in duplicates_removed)
            if not duplicate:
                duplicates_removed.append(product)

        return duplicates_removed
