from controllers.item_controller import ItemController


class Product:
    def __init__(self, recipe_id, item_id, quantity, cost, sell_price,
                 sell_frequency) -> None:
        self.recipe_id = recipe_id
        item = ItemController.get_item(item_id)
        self.name = item.sort_name.replace("_", " ").title()
        self.quantity = quantity
        self.cost = cost
        self.sell_price = sell_price
        self.sell_frequency = sell_frequency
        self.profit = sell_price - cost
