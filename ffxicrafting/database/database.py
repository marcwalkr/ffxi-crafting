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

    def get_auction_items(self, item_id: int) -> list:
        """
        Retrieve auction items for a specific item ID.

        Args:
            item_id (int): The ID of the item to retrieve auction data for.

        Returns:
            list: A list of auction items for the specified item ID.
        """
        query = "SELECT * FROM auction_items WHERE itemid=%s AND no_sale=0"
        return self._execute_query(query, (item_id,), fetch_one=False)

    def update_auction_item(self, item_id: int, avg_price: int, sell_freq: float, is_stack: int) -> None:
        """
        Update the auction data for a specific item.

        Args:
            item_id (int): The ID of the item to update.
            avg_price (int): The new average price for the item.
            sell_freq (float): The new sell frequency for the item.
            is_stack (int): Indicates whether the item is a stack (1) or single (0).
        """
        query = "UPDATE auction_items SET avg_price = %s, sell_freq = %s, new_data = 0 "
        query += "WHERE itemid = %s AND is_stack = %s"
        return self._execute_query(query, (avg_price, sell_freq, item_id, is_stack), commit=True)

    def get_latest_sales_history(self, item_id: int, is_stack: int) -> list:
        """
        Retrieve the latest sales history for a specific item.

        Args:
            item_id (int): The ID of the item to retrieve sales history for.
            is_stack (int): Indicates whether to retrieve history for stacks (1) or singles (0).

        Returns:
            list: A list of the latest sales history entries for the specified item.
        """
        query = "SELECT * FROM sales_history WHERE itemid=%s AND is_stack=%s AND batch_id = "
        query += "(SELECT MAX(batch_id) FROM sales_history WHERE itemid=%s AND is_stack=%s)"
        return self._execute_query(query, (item_id, is_stack, item_id, is_stack), fetch_one=False)

    def get_guild_shops(self, item_id: int) -> list:
        """
        Retrieve guild shop data for a specific item.

        Args:
            item_id (int): The ID of the item to retrieve guild shop data for.

        Returns:
            list: A list of guild shop entries for the specified item.
        """
        query = "SELECT * FROM guild_shops WHERE itemid=%s"
        return self._execute_query(query, (item_id,), fetch_one=False)

    def get_guild_vendor(self, guild_id: int) -> tuple:
        """
        Retrieve information for a specific guild vendor.

        Args:
            guild_id (int): The ID of the guild vendor to retrieve information for.

        Returns:
            tuple: A tuple containing the guild vendor information.
        """
        query = "SELECT * FROM guild_vendors WHERE guildid=%s"
        return self._execute_query(query, (guild_id,), fetch_one=True)

    def get_items(self, item_ids: list[int]) -> list:
        """
        Retrieve item data for a list of item IDs.

        Args:
            item_ids (list[int]): A list of item IDs to retrieve data for.

        Returns:
            list: A list of item data for the specified item IDs.
        """
        format_strings = ",".join(["%s"] * len(item_ids))
        query = f"SELECT * FROM item_basic WHERE itemid IN ({format_strings})"
        return self._execute_query(query, tuple(item_ids), fetch_one=False)

    def get_npc(self, npc_id: int) -> tuple:
        """
        Retrieve information for a specific NPC.

        Args:
            npc_id (int): The ID of the NPC to retrieve information for.

        Returns:
            tuple: A tuple containing the NPC information.
        """
        query = "SELECT * FROM npc_list WHERE npcid=%s"
        return self._execute_query(query, (npc_id,), fetch_one=True)

    def get_recipes_by_level(self, wood: int, smith: int, gold: int, cloth: int, leather: int, bone: int,
                             alchemy: int, cook: int, batch_size: int, offset: int) -> list:
        """
        Retrieve recipes based on crafting skill levels.

        Args:
            wood (int): Woodworking crafting skill level.
            smith (int): Smithing crafting skill level.
            gold (int): Goldsmithing crafting skill level.
            cloth (int): Clothcraft crafting skill level.
            leather (int): Leatherworking crafting skill level.
            bone (int): Bonecraft crafting skill level.
            alchemy (int): Alchemy crafting skill level.
            cook (int): Cooking crafting skill level.
            batch_size (int): Number of recipes to retrieve.
            offset (int): Offset for pagination.

        Returns:
            list: A list of recipes matching the specified crafting skill levels.
        """
        query = ("SELECT * FROM synth_recipes WHERE wood <= %s AND smith <= %s AND gold <= %s AND cloth <= %s "
                 "AND leather <= %s AND bone <= %s AND alchemy <= %s AND cook <= %s LIMIT %s OFFSET %s")
        return self._execute_query(query, (wood, smith, gold, cloth, leather, bone, alchemy, cook, batch_size, offset), fetch_one=False)

    def search_recipe(self, search_term: str, batch_size: int, offset: int) -> list:
        """
        Search for recipes based on a search term.

        Args:
            search_term (str): The term to search for in recipe names.
            batch_size (int): Number of recipes to retrieve.
            offset (int): Offset for pagination.

        Returns:
            list: A list of recipes matching the search term.
        """
        query = """
        SELECT * FROM synth_recipes
        WHERE MATCH(ResultName) AGAINST(%s IN BOOLEAN MODE)
        ORDER BY MATCH(ResultName) AGAINST(%s IN BOOLEAN MODE) DESC, ID ASC
        LIMIT %s OFFSET %s;
        """
        return self._execute_query(query, (search_term, search_term, batch_size, offset), fetch_one=False)

    def get_all_result_item_ids(self) -> list:
        """
        Retrieve all unique result item IDs from the recipes.

        Returns:
            list: A list of all unique result item IDs.
        """
        query = """
        SELECT DISTINCT result_id FROM (
            SELECT result AS result_id FROM synth_recipes WHERE result IS NOT NULL
            UNION
            SELECT resulthq1 AS result_id FROM synth_recipes WHERE resulthq1 IS NOT NULL
            UNION
            SELECT resulthq2 AS result_id FROM synth_recipes WHERE resulthq2 IS NOT NULL
            UNION
            SELECT resulthq3 AS result_id FROM synth_recipes WHERE resulthq3 IS NOT NULL
        ) AS all_results
        """
        results = self._execute_query(query, (), fetch_one=False)
        return [result[0] for result in results]

    def get_regional_vendor(self, npc_id: int) -> tuple:
        """
        Retrieve information for a specific regional vendor.

        Args:
            npc_id (int): The ID of the regional vendor to retrieve information for.

        Returns:
            tuple: A tuple containing the regional vendor information.
        """
        query = "SELECT * FROM regional_vendors WHERE npcid=%s"
        return self._execute_query(query, (npc_id,), fetch_one=True)

    def get_vendor_items(self, item_id: int) -> list:
        """
        Retrieve vendor items for a specific item ID.

        Args:
            item_id (int): The ID of the item to retrieve vendor data for.

        Returns:
            list: A list of vendor items for the specified item ID.
        """
        query = "SELECT * FROM vendor_items WHERE itemid=%s"
        return self._execute_query(query, (item_id,), fetch_one=False)

    def get_vendor_location(self, npc_id: int) -> tuple:
        """
        Retrieve location information for a specific vendor.

        Args:
            npc_id (int): The ID of the vendor to retrieve location information for.

        Returns:
            tuple: A tuple containing the vendor location information.
        """
        query = "SELECT * FROM vendor_locations WHERE npcid=%s"
        return self._execute_query(query, (npc_id,), fetch_one=True)
