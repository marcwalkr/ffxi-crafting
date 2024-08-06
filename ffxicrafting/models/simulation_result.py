from datetime import datetime


class SimulationResult:
    """
    Represents the result of a crafting simulation in FFXI.

    This class corresponds to a database table that stores simulation data,
    including crafting details, game world conditions, and economic factors
    that affect the crafting process and its outcomes.
    """

    def __init__(self, item_id: int, recipe_id: int, crafter_tier: int, beastmen_regions: str, conquest_ranking: str,
                 enabled_guilds: str, from_scratch: bool, synth_cost: float, simulation_cost: float, quantity: int,
                 last_updated: datetime) -> None:
        """
        Initialize a SimulationResult instance.

        Args:
            item_id (int): The ID of the item crafted in the simulation.
            recipe_id (int): The ID of the recipe used for crafting.
            crafter_tier (int): An integer from -1 to 3 representing the synthesis difficulty,
                                which affects the crafting results.
            beastmen_regions (str): A JSON string representing the regions controlled by beastmen, 
                                    affecting vendor item availability.
            conquest_ranking (str): A JSON string representing the ranking of each nation in the conquest,
                                    affecting vendor item availability.
            enabled_guilds (str): A JSON string representing the list of guilds enabled by the user,
                                  affecting item prices as items may need to be obtained from alternative sources.
            from_scratch (bool): Whether the item was crafted "from scratch" by crafting
                                 all craftable ingredients in the recipe.
            synth_cost (float): The sum of the recipe's ingredient prices.
            simulation_cost (float): The total cost of the entire simulation from all trials,
                                     with retained ingredient costs subtracted after failures.
            quantity (int): The quantity of the item produced in the simulation.

            last_updated (datetime): When the database row was last updated.
        """
        self.item_id: int = item_id
        self.recipe_id: int = recipe_id
        self.crafter_tier: int = crafter_tier
        self.beastmen_regions: str = beastmen_regions
        self.conquest_ranking: str = conquest_ranking
        self.enabled_guilds: str = enabled_guilds
        self.from_scratch: bool = from_scratch
        self.synth_cost: float = synth_cost
        self.simulation_cost: float = simulation_cost
        self.quantity: int = quantity
        self.last_updated: datetime = last_updated
