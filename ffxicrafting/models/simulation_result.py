from datetime import datetime


class SimulationResult:
    """
    Represents the result of a crafting simulation in FFXI.

    This class corresponds to a database table that stores simulation data,
    including crafting details, costs, and quantities of the item produced.
    """

    def __init__(self, item_id: int, recipe_id: int, crafter_tier: int, min_cost_used: bool, synth_cost: float,
                 simulation_cost: float, leftover_cost: float, quantity: int, cost_per_unit: float,
                 last_updated: datetime) -> None:
        """
        Initialize a SimulationResult instance.

        Args:
            item_id (int): The ID of the item crafted in the simulation.
            recipe_id (int): The ID of the recipe used for crafting.
            crafter_tier (int): An integer from -1 to 3 representing the synthesis difficulty.
            min_cost_used (bool): Whether the minimum cost was used for the simulation.
            synth_cost (float): The sum of the recipe's ingredient prices.
            simulation_cost (float): The total cost of the entire simulation from all trials.
            leftover_cost (float): The cost of the ingredients that were retained after failures.
            quantity (int): The quantity of the item produced in the simulation.
            cost_per_unit (float): The cost per unit of the item produced.
            last_updated (datetime): When the database row was last updated.
        """
        self.item_id: int = item_id
        self.recipe_id: int = recipe_id
        self.crafter_tier: int = crafter_tier
        self.min_cost_used: bool = min_cost_used
        self.synth_cost: float = synth_cost
        self.simulation_cost: float = simulation_cost
        self.leftover_cost: float = leftover_cost
        self.quantity: int = quantity
        self.cost_per_unit: float = cost_per_unit
        self.last_updated: datetime = last_updated
