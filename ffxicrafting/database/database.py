import threading
import logging
import time
from mysql.connector import pooling, errors
from mysql.connector.cursor import MySQLCursor
from config.settings_manager import SettingsManager

logger = logging.getLogger(__name__)


class Database:
    """
    A class for managing database connections and executing queries.
    """

    _pool: pooling.MySQLConnectionPool = None
    _pool_lock: threading.Lock = threading.Lock()
    _local: threading.local = threading.local()
    _max_retries: int = 3
    _retry_delay: int = 5

    @classmethod
    def _initialize_pool(cls) -> None:
        """
        Initialize the database connection pool.

        Creates a new connection pool if one doesn't exist, using settings from SettingsManager.
        Retries the connection attempt up to _max_retries times if it fails.

        Raises:
            Exception: If the database configuration is incomplete or connection attempts fail.
        """
        with cls._pool_lock:
            if cls._pool is None:
                config = {
                    "host": SettingsManager.get_database_host(),
                    "user": SettingsManager.get_database_user(),
                    "password": SettingsManager.get_database_password(),
                    "database": SettingsManager.get_database_name()
                }

                if not all(config.values()):
                    logger.error("Database configuration is incomplete")
                    raise

                for attempt in range(cls._max_retries):
                    try:
                        cls._pool = pooling.MySQLConnectionPool(
                            pool_name="mypool",
                            pool_size=32,
                            **config
                        )
                        return
                    except errors.DatabaseError as e:
                        logger.warning(f"Database connection attempt {attempt + 1} failed: {e}")
                        if attempt < cls._max_retries - 1:
                            logger.info(f"Retrying in {cls._retry_delay} seconds...")
                            time.sleep(cls._retry_delay)
                        else:
                            logger.error("Failed to initialize database connection pool after maximum retries")
                            raise

    @classmethod
    def _get_connection(cls) -> tuple[pooling.MySQLConnection, MySQLCursor]:
        """
        Get a database connection and cursor from the pool.

        Initializes the connection pool if it doesn't exist, then retrieves a connection
        and creates a cursor.

        Returns:
            tuple[pooling.MySQLConnection, pooling.MySQLCursor]: A tuple containing the database
            connection and cursor.

        Raises:
            errors.DatabaseError: If unable to get a database connection.
        """
        if not hasattr(cls._local, "connection") or cls._local.connection is None:
            try:
                cls._initialize_pool()
                cls._local.connection = cls._pool.get_connection()
                cls._local.cursor = cls._local.connection.cursor(buffered=True)
            except errors.DatabaseError as e:
                logger.error(f"Failed to get database connection: {e}")
                raise
        return cls._local.connection, cls._local.cursor

    @classmethod
    def close_connection(cls) -> None:
        """
        Close the current database connection and cursor.

        Closes the cursor and connection associated with the current thread, if they exist.
        """
        if hasattr(cls._local, "connection") and cls._local.connection is not None:
            cls._local.cursor.close()
            cls._local.connection.close()
            cls._local.connection = None
            cls._local.cursor = None

    def __enter__(self) -> None:
        """
        Enter the runtime context for the Database instance.

        Acquires a database connection when entering a 'with' statement.

        Returns:
            Database: The Database instance.
        """
        self._get_connection()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the runtime context for the Database instance.

        Closes the database connection when exiting a 'with' statement.

        Args:
            exc_type: The exception type, if an exception was raised in the 'with' block.
            exc_val: The exception value, if an exception was raised in the 'with' block.
            exc_tb: The traceback, if an exception was raised in the 'with' block.
        """
        self.close_connection()

    def _execute_query(self, query: str, params: tuple = None, fetch_one: bool = False, commit: bool = False) -> list | tuple | None:
        """
        Execute a SQL query and return the results.

        Args:
            query (str): The SQL query to execute.
            params (tuple, optional): Parameters to be used with the query. Defaults to None.
            fetch_one (bool, optional): If True, fetches only one result. Defaults to False.
            commit (bool, optional): If True, commits the transaction. Defaults to False.

        Returns:
            list | tuple | None: The query results as a list of tuples, a single tuple, or None.

        Raises:
            errors.Error: If the database query fails.
        """
        try:
            connection, cursor = self._get_connection()
            cursor.execute(query, params)

            if commit:
                connection.commit()
                return None
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall() or []
        except errors.Error as e:
            if commit:
                connection.rollback()
            logger.error(f"Database query failed: {e}")
            return None if fetch_one else []

    def get_all_auction_items(self) -> list:
        """
        Retrieve all auction items.

        Returns:
            list: A list of all auction items.
        """
        query = "SELECT itemid, avg_price, num_sales, sell_freq, is_stack, new_data FROM auction_items"
        return self._execute_query(query, (), fetch_one=False)

    def get_all_sales_history(self) -> list:
        """
        Retrieve all the latest sales history.

        Returns:
            list: A list of all the latest sales history.
        """
        query = "SELECT itemid, is_stack, price, batch_id FROM sales_history"
        return self._execute_query(query, (), fetch_one=False)

    def get_all_guild_shops(self) -> list:
        """
        Retrieve all guild shop data.

        Returns:
            list: A list of all guild shop data.
        """
        query = "SELECT guildid, itemid, min_price, max_price, daily_increase, initial_quantity FROM guild_shops"
        return self._execute_query(query, (), fetch_one=False)

    def get_all_guild_vendors(self) -> list:
        """
        Retrieve all guild vendor data.

        Returns:
            list: A list of all guild vendor data.
        """
        query = "SELECT * FROM guild_vendors"
        return self._execute_query(query, (), fetch_one=False)

    def get_items(self, item_ids: list[int]) -> list:
        """
        Retrieve item data for a list of item IDs.

        Args:
            item_ids (list[int]): A list of item IDs to retrieve data for.

        Returns:
            list: A list of item data for the specified item IDs.
        """
        format_strings = ",".join(["%s"] * len(item_ids))
        query = f"SELECT itemid, name, sortname, stackSize FROM item_basic WHERE itemid IN ({format_strings})"
        return self._execute_query(query, tuple(item_ids), fetch_one=False)

    def get_all_vendor_npcs(self) -> list:
        """
        Retrieve all vendor NPCs.

        Returns:
            list: A list of all vendor NPCs.
        """
        query = "SELECT polutils_name FROM npc_list WHERE npcid IN (SELECT npcid FROM vendor_locations)"
        return self._execute_query(query, (), fetch_one=False)

    def get_all_recipes(self) -> list:
        """
        Retrieve all recipes.

        Returns:
            list: A list of all recipes.
        """
        query = "SELECT ID, Desynth, KeyItem, Wood, Smith, Gold, Cloth, Leather, Bone, Alchemy, Cook, Crystal, "
        query += "Ingredient1, Ingredient2, Ingredient3, Ingredient4, Ingredient5, Ingredient6, Ingredient7, "
        query += "Ingredient8, Result, ResultHQ1, ResultHQ2, ResultHQ3, ResultQty, ResultHQ1Qty, ResultHQ2Qty, "
        query += "ResultHQ3Qty, ResultName FROM synth_recipes"
        return self._execute_query(query, (), fetch_one=False)

    def get_all_recipe_item_ids(self) -> list:
        """
        Retrieve all unique non-zero item IDs from the recipes, including crystals, ingredients, results.

        Returns:
            list: A list of all unique non-zero item IDs used in recipes.
        """
        query = """
        SELECT DISTINCT item_id FROM (
            SELECT Crystal AS item_id FROM synth_recipes WHERE Crystal != 0
            UNION
            SELECT Ingredient1 FROM synth_recipes WHERE Ingredient1 != 0
            UNION
            SELECT Ingredient2 FROM synth_recipes WHERE Ingredient2 != 0
            UNION
            SELECT Ingredient3 FROM synth_recipes WHERE Ingredient3 != 0
            UNION
            SELECT Ingredient4 FROM synth_recipes WHERE Ingredient4 != 0
            UNION
            SELECT Ingredient5 FROM synth_recipes WHERE Ingredient5 != 0
            UNION
            SELECT Ingredient6 FROM synth_recipes WHERE Ingredient6 != 0
            UNION
            SELECT Ingredient7 FROM synth_recipes WHERE Ingredient7 != 0
            UNION
            SELECT Ingredient8 FROM synth_recipes WHERE Ingredient8 != 0
            UNION
            SELECT Result FROM synth_recipes WHERE Result != 0
            UNION
            SELECT ResultHQ1 FROM synth_recipes WHERE ResultHQ1 != 0
            UNION
            SELECT ResultHQ2 FROM synth_recipes WHERE ResultHQ2 != 0
            UNION
            SELECT ResultHQ3 FROM synth_recipes WHERE ResultHQ3 != 0
        ) AS all_items
        """
        results = self._execute_query(query, (), fetch_one=False)
        return [result[0] for result in results]

    def get_all_regional_vendors(self) -> list:
        """
        Retrieve all regional vendors.

        Returns:
            list: A list of all regional vendors.
        """
        query = "SELECT * FROM regional_vendors"
        return self._execute_query(query, (), fetch_one=False)

    def get_all_vendor_items(self) -> list:
        """
        Retrieve all vendor items.

        Returns:
            list: A list of all vendor items.
        """
        query = "SELECT * FROM vendor_items"
        return self._execute_query(query, (), fetch_one=False)

    def get_all_vendor_locations(self) -> list:
        """
        Retrieve all vendor locations.

        Returns:
            list: A list of all vendor locations.
        """
        query = "SELECT * FROM vendor_locations"
        return self._execute_query(query, (), fetch_one=False)

    def get_all_zones(self) -> list:
        """
        Retrieve all zones.

        Returns:
            list: A list of all zones.
        """
        query = "SELECT zoneid, name FROM zone_settings"
        return self._execute_query(query, (), fetch_one=False)
