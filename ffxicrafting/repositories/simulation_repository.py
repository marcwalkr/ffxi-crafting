from threading import Lock
from database import Database
from models import SimulationResult


class SimulationRepository:
    """
    Repository class for handling crafting simulation data operations.

    This class provides methods to interact with the database for retrieving,
    inserting, and updating simulation results. It implements caching to improve
    performance for frequently accessed simulation data.
    """

    _cache: dict[tuple[int, int, int, bool], SimulationResult] = {}
    _cache_lock: Lock = Lock()

    def __init__(self, db: Database) -> None:
        """
        Initialize a SimulationRepository instance.

        Args:
            db (Database): The database connection object used for querying simulation data.
        """
        self._db: Database = db

    def get_simulation_result(self, item_id: int, recipe_id: int, crafter_tier: int,
                              min_cost_used: bool) -> SimulationResult | None:
        """
        Retrieve a simulation result for given parameters.

        This method first checks the cache for the requested simulation result. If not found,
        it queries the database and caches the result for future use.

        Args:
            item_id (int): The ID of the crafted item.
            recipe_id (int): The ID of the recipe used.
            crafter_tier (int): The tier of the crafter who crafted the recipe.
            min_cost_used (bool): Whether the minimum cost was used.

        Returns:
            SimulationResult | None: A SimulationResult object if found, None otherwise.
        """
        cache_key = (item_id, recipe_id, crafter_tier, min_cost_used)
        if cache_key in self._cache:
            return self._cache[cache_key]

        result_tuple = self._db.get_simulation_result(item_id, recipe_id, crafter_tier, min_cost_used)
        if result_tuple:
            simulation_result = SimulationResult(*result_tuple)
            self._cache[cache_key] = simulation_result
            return simulation_result
        else:
            return None

    def insert_simulation_result(self, item_id: int, recipe_id: int, crafter_tier: int, min_cost_used: bool,
                                 synth_cost: float, simulation_cost: float, leftover_cost: float, quantity: int,
                                 cost_per_unit: float) -> None:
        """
        Insert a new simulation result into the database and cache.

        Args:
            item_id (int): The ID of the crafted item.
            recipe_id (int): The ID of the recipe used.
            crafter_tier (int): The tier of the crafter who crafted the recipe.
            min_cost_used (bool): Whether the minimum cost was used.
            synth_cost (float): The sum of the recipe's ingredient prices.
            simulation_cost (float): The total cost of the entire simulation from all trials.
            leftover_cost (float): The cost of the ingredients that were retained after failures.
            quantity (int): The quantity of items produced.
            cost_per_unit (float): The cost per unit of the item produced.
        """
        self._db.insert_simulation_result(item_id, recipe_id, crafter_tier, min_cost_used, synth_cost,
                                          simulation_cost, leftover_cost, quantity, cost_per_unit)
        cache_key = (item_id, recipe_id, crafter_tier, min_cost_used)
        self._cache[cache_key] = SimulationResult(item_id, recipe_id, crafter_tier, min_cost_used, synth_cost,
                                                  simulation_cost, leftover_cost, quantity, cost_per_unit)

    def update_simulation_result(self, item_id: int, recipe_id: int, crafter_tier: int, min_cost_used: bool,
                                 synth_cost: float, simulation_cost: float, leftover_cost: float, quantity: int,
                                 cost_per_unit: float) -> None:
        """
        Update an existing simulation result in the database and invalidate the cache for the result.

        Args:
            item_id (int): The ID of the crafted item.
            recipe_id (int): The ID of the recipe used.
            crafter_tier (int): The tier of the crafter who crafted the recipe.
            min_cost_used (bool): Whether the minimum cost was used.
            synth_cost (float): The sum of the recipe's ingredient prices.
            simulation_cost (float): The total cost of the entire simulation from all trials.
            leftover_cost (float): The cost of the ingredients that were retained after failures.
            quantity (int): The quantity of items produced.
            cost_per_unit (float): The cost per unit of the item produced.
        """
        self._db.update_simulation_result(item_id, recipe_id, crafter_tier, min_cost_used, synth_cost,
                                          simulation_cost, leftover_cost, quantity, cost_per_unit)
        self._invalidate_cache(item_id, recipe_id, crafter_tier, min_cost_used)

    def _invalidate_cache(self, item_id: int, recipe_id: int, crafter_tier: int, min_cost_used: bool) -> None:
        """
        Invalidate the cache for a specific simulation result.
        """
        cache_key = (item_id, recipe_id, crafter_tier, min_cost_used)
        with self._cache_lock:
            self._cache.pop(cache_key, None)
