from entities import Item, CraftableItem


class Ingredient(Item):
    """
    Represents an ingredient item in the game, extending the base Item class with additional
    properties specific to ingredients used in crafting.
    """

    def __init__(self, *args) -> None:
        """Initialize an Ingredient instance."""
        super().__init__(*args)
        self.vendor_cost: int | None = None
        self.guild_cost: int | None = None

    def get_min_cost(self) -> int | float | None:
        """
        Calculate the minimum cost of the ingredient from various sources.

        Returns:
            int | float | None: The lowest cost among vendor cost, guild cost, single price,
            and stack price (divided by stack size). Returns None if no valid costs are available.
        """
        if self.stack_price is not None:
            cost_from_stack = self.stack_price / self.stack_size
        else:
            cost_from_stack = None

        costs = [self.vendor_cost, self.guild_cost, self.single_price, cost_from_stack]
        valid_costs = [cost for cost in costs if cost is not None]

        return min(valid_costs, default=None)


class CraftableIngredient(Ingredient, CraftableItem):
    """
    Represents an ingredient that can also be crafted, combining properties of both
    Ingredient and CraftableItem classes.
    """

    def __init__(self, *args) -> None:
        """Initialize a CraftableIngredient instance."""
        super().__init__(*args)
        self.crafted_cost: float | None = None

    def get_min_cost(self) -> int | float | None:
        """
        Calculate the minimum cost of the craftable ingredient from various sources,
        including its crafted cost.

        Returns:
            int | float | None: The lowest cost among vendor cost, guild cost, single price,
            stack price (divided by stack size), and crafted cost. Returns None if no valid
            costs are available.
        """
        costs = [super().get_min_cost(), self.crafted_cost]
        valid_costs = [cost for cost in costs if cost is not None]
        return min(valid_costs, default=None)
