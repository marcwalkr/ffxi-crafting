from entities import Item, CraftableItem


class Ingredient(Item):
    instances = []

    def __init__(self, item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell):
        super().__init__(item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell)
        self.vendor_cost = None
        self.guild_cost = None
        Ingredient.instances.append(self)

    def get_min_cost(self):
        if self.stack_price is not None:
            cost_from_stack = self.stack_price / self.stack_size
        else:
            cost_from_stack = None

        costs = [self.vendor_cost, self.guild_cost, self.single_price, cost_from_stack]
        costs = [cost for cost in costs if cost is not None]

        return min(costs, default=None)


class CraftableIngredient(Ingredient, CraftableItem):
    instances = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        CraftableIngredient.instances.append(self)

    def get_min_cost(self):
        costs = super().get_min_cost()
        if self.crafted_cost is not None:
            costs = min(costs, self.crafted_cost)
        return costs
