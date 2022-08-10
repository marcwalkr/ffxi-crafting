class Product:
    def __init__(self, recipe_id, name, quantity, cost, sell_price,
                 sell_frequency) -> None:
        self.recipe_id = recipe_id
        self.name = name
        self.quantity = quantity
        self.cost = cost
        self.sell_price = sell_price
        self.sell_frequency = sell_frequency
        self.profit = sell_price - cost
