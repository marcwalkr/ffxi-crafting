import json
from database import Database
from models import SimulationResult
from config import SettingsManager


class SimulationRepository:
    """
    Repository class for handling crafting simulation data operations.

    This class provides methods to interact with the database for retrieving,
    inserting, and updating simulation results. It implements caching to improve
    performance for frequently accessed simulation data.
    """

    _cache: dict[tuple[int, int, int, str, str, str, bool], SimulationResult] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize a SimulationRepository instance.

        Args:
            db (Database): The database connection object used for querying simulation data.
        """
        self._db: Database = db
        self._beastmen_regions: str = json.dumps(SettingsManager.get_beastmen_regions())
        self._conquest_ranking: str = json.dumps(SettingsManager.get_conquest_ranking())
        self._enabled_guilds: str = json.dumps(SettingsManager.get_enabled_guilds())

    def get_simulation_result(self, item_id: int, recipe_id: int, crafter_tier: int,
                              from_scratch: bool) -> SimulationResult | None:
        """
        Retrieve a simulation result for given parameters.

        This method first checks the cache for the requested simulation result. If not found,
        it queries the database and caches the result for future use.

        Args:
            item_id (int): The ID of the crafted item.
            recipe_id (int): The ID of the recipe used.
            crafter_tier (int): The tier of the crafter who crafted the recipe.
            from_scratch (bool): Whether the ingredients for the recipe were also crafted.

        Returns:
            SimulationResult | None: A SimulationResult object if found, None otherwise.
        """
        cache_key = (item_id, recipe_id, crafter_tier, self._beastmen_regions,
                     self._conquest_ranking, self._enabled_guilds, from_scratch)
        if cache_key in self._cache:
            return self._cache[cache_key]

        result_tuple = self._db.get_simulation_result(item_id, recipe_id, crafter_tier, self._beastmen_regions,
                                                      self._conquest_ranking, self._enabled_guilds, from_scratch)
        if result_tuple:
            simulation_result = SimulationResult(*result_tuple)
            self._cache[cache_key] = simulation_result
            return simulation_result
        else:
            return None

    def insert_simulation_result(self, item_id: int, recipe_id: int, crafter_tier: int, from_scratch: bool,
                                 synth_cost: float, simulation_cost: float, quantity: int) -> None:
        """
        Insert a new simulation result into the database and cache.

        Args:
            item_id (int): The ID of the crafted item.
            recipe_id (int): The ID of the recipe used.
            crafter_tier (int): The tier of the crafter who crafted the recipe.
            from_scratch (bool): Whether the ingredients for the recipe were also crafted.
            synth_cost (float): The sum of the recipe's ingredient prices.
            simulation_cost (float): The total cost of the entire simulation from all trials,
                                     with retained ingredient costs subtracted after failures.
            quantity (int): The quantity of items produced.
        """
        self._db.insert_simulation_result(item_id, recipe_id, crafter_tier, self._beastmen_regions,
                                          self._conquest_ranking, self._enabled_guilds, from_scratch, synth_cost,
                                          simulation_cost, quantity)
        cache_key = (item_id, recipe_id, crafter_tier, self._beastmen_regions,
                     self._conquest_ranking, self._enabled_guilds, from_scratch)
        self._cache[cache_key] = SimulationResult(item_id, recipe_id, crafter_tier, self._beastmen_regions,
                                                  self._conquest_ranking, self._enabled_guilds, from_scratch,
                                                  synth_cost, simulation_cost, quantity)

    def delete_simulation_result(self, simulation_result: SimulationResult) -> None:
        """
        Delete an existing simulation result from the database and cache.

        Args:
            simulation_result (SimulationResult): The SimulationResult object with updated information.
        """
        self._db.delete_simulation_result(simulation_result.item_id, simulation_result.recipe_id,
                                          simulation_result.crafter_tier, simulation_result.beastmen_regions,
                                          simulation_result.conquest_ranking, simulation_result.enabled_guilds,
                                          simulation_result.from_scratch)
        cache_key = (simulation_result.item_id, simulation_result.recipe_id, simulation_result.crafter_tier,
                     simulation_result.beastmen_regions, simulation_result.conquest_ranking,
                     simulation_result.enabled_guilds, simulation_result.from_scratch)
        del self._cache[cache_key]
