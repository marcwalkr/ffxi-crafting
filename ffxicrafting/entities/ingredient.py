from entities import Item, CraftableItem


class Ingredient(Item):
    def __init__(self, item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell):
        super().__init__(item_id, sub_id, name, sort_name, stack_size, flags, ah, no_sale, base_sell)
        self.vendor_cost = None
        self.guild_cost = None

    def get_min_cost(self):
        if self.stack_price is not None:
            cost_from_stack = self.stack_price / self.stack_size
        else:
            cost_from_stack = None

        costs = [self.vendor_cost, self.guild_cost, self.single_price, cost_from_stack]
        valid_costs = [cost for cost in costs if cost is not None]

        return min(valid_costs, default=None)


class CraftableIngredient(Ingredient, CraftableItem):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_min_cost(self):
        costs = [super().get_min_cost(), self.crafted_cost]
        valid_costs = [cost for cost in costs if cost is not None]
        return min(valid_costs, default=None)
