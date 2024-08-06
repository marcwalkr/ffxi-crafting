from datetime import datetime


class SimulationResult:
    """
    Represents the result of a crafting simulation in FFXI.

    This class corresponds to a database table that stores simulation data,
    including crafting details, game world conditions, and economic factors
    that affect the crafting process and its outcomes.
    """

    def __init__(self, item_id: int, recipe_id: int, crafter_tier: int, beastmen_regions: list[str],
                 conquest_ranking: dict[str, str], enabled_guilds: list[str], synth_cost: float,
                 simulation_cost: float, quantity: int, from_scratch: bool, last_updated: datetime) -> None:
        """
        Initialize a SimulationResult instance.

        Args:
            item_id (int): The ID of the item crafted in the simulation.
            recipe_id (int): The ID of the recipe used for crafting.
            crafter_tier (int): An integer from -1 to 3 representing the synthesis difficulty,
                                which affects the crafting results.
            beastmen_regions (list[str]): A list of regions controlled by beastmen,
                                          affecting vendor item availability.
            conquest_ranking (dict[str, str]): The ranking of each nation in the conquest,
                                               affecting vendor item availability.
            enabled_guilds (list[str]): A list of guilds enabled by the user, affecting item prices
                                        as items may need to be obtained from alternative sources.
            synth_cost (float): The sum of the recipe's ingredient prices.
            simulation_cost (float): The total cost of the entire simulation from all trials,
                                     with retained ingredient costs subtracted after failures.
            quantity (int): The quantity of the item produced in the simulation.
            from_scratch (bool): Whether the item was crafted "from scratch" by crafting
                                 all craftable ingredients in the recipe.
            last_updated (datetime): When the database row was last updated.
        """
        self.item_id: int = item_id
        self.recipe_id: int = recipe_id
        self.crafter_tier: int = crafter_tier
        self.beastmen_regions: list[str] = beastmen_regions
        self.conquest_ranking: dict[str, str] = conquest_ranking
        self.enabled_guilds: list[str] = enabled_guilds
        self.synth_cost: float = synth_cost
        self.simulation_cost: float = simulation_cost
        self.quantity: int = quantity
        self.from_scratch: bool = from_scratch
        self.last_updated: datetime = last_updated
