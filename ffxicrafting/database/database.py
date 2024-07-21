import threading
import warnings
from mysql.connector import pooling
from config.settings_manager import SettingsManager


class Database:
    _pool = None
    _pool_lock = threading.Lock()

    @classmethod
    def initialize_pool(cls):
        host = SettingsManager.get_database_host()
        user = SettingsManager.get_database_user()
        password = SettingsManager.get_database_password()
        database = SettingsManager.get_database_name()

        if not all([host, user, password, database]):
            warnings.warn("Database configuration is incomplete")
            cls._pool = None
            return

        if cls._pool is None:
            with cls._pool_lock:
                if cls._pool is None:  # Double-checked locking
                    cls._pool = pooling.MySQLConnectionPool(
                        pool_name="mypool",
                        pool_size=20,
                        host=host,
                        user=user,
                        password=password,
                        database=database
                    )

    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def _connect(self):
        if self.connection is None:
            if self._pool is None:
                self.initialize_pool()
            if self._pool:
                try:
                    self.connection = self._pool.get_connection()
                    self.cursor = self.connection.cursor(buffered=True)
                except Exception as e:
                    warnings.warn(f"Failed to connect to database: {e}")
                    self._pool = None
                    raise DatabaseException(
                        "Failed to connect to the database. Please check the configuration and try again.")

    def execute_query(self, query, params, fetch_method="all", commit=False):
        self._connect()
        if not self.cursor:
            raise DatabaseException("Database not connected. Please check the configuration and try again.")
        try:
            self.cursor.execute(query, params)
            if commit:
                self.connection.commit()
                return
            if fetch_method == "one":
                return self.cursor.fetchone()
            elif fetch_method == "none":
                return None
            else:
                result = self.cursor.fetchall()
                return result if result is not None else []
        except Exception as e:
            self.connection.rollback()
            raise e

    def db_connection_required(func):
        def wrapper(self, *args, **kwargs):
            self._connect()
            return func(self, *args, **kwargs)
        return wrapper

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    @db_connection_required
    def get_auction_items(self, item_id):
        query = "SELECT * FROM auction_items WHERE itemid=%s AND no_sale=0"
        return self.execute_query(query, (item_id,), fetch_method="all")

    @db_connection_required
    def update_auction_item(self, item_id, avg_price, sell_freq, is_stack):
        query = "UPDATE auction_items SET avg_price = %s, sell_freq = %s, new_data = 0 "
        query += "WHERE itemid = %s AND is_stack = %s"
        return self.execute_query(query, (avg_price, sell_freq, item_id, is_stack), commit=True)

    @db_connection_required
    def get_latest_sales_history(self, item_id, is_stack):
        query = "SELECT * FROM sales_history WHERE itemid=%s AND is_stack=%s AND batch_id = "
        query += "(SELECT MAX(batch_id) FROM sales_history WHERE itemid=%s AND is_stack=%s)"
        return self.execute_query(query, (item_id, is_stack, item_id, is_stack), fetch_method="all")

    @db_connection_required
    def get_guild_shops(self, item_id):
        query = "SELECT * FROM guild_shops WHERE itemid=%s"
        return self.execute_query(query, (item_id,), fetch_method="all")

    @db_connection_required
    def get_guild_vendor(self, guild_id):
        query = "SELECT * FROM guild_vendors WHERE guildid=%s"
        return self.execute_query(query, (guild_id,), fetch_method="one")

    @db_connection_required
    def get_item(self, item_id):
        query = "SELECT * FROM item_basic WHERE itemid=%s"
        return self.execute_query(query, (item_id,), fetch_method="one")

    @db_connection_required
    def get_items(self, item_ids):
        format_strings = ','.join(['%s'] * len(item_ids))
        query = f"SELECT * FROM item_basic WHERE itemid IN ({format_strings})"
        return self.execute_query(query, tuple(item_ids), fetch_method="all")

    @db_connection_required
    def get_npc(self, npc_id):
        query = "SELECT * FROM npc_list WHERE npcid=%s"
        return self.execute_query(query, (npc_id,), fetch_method="one")

    @db_connection_required
    def get_recipe(self, recipe_id):
        query = "SELECT * FROM synth_recipes WHERE id=%s"
        return self.execute_query(query, (recipe_id,), fetch_method="one")

    @db_connection_required
    def get_recipes_by_level(self, wood, smith, gold, cloth, leather, bone, alchemy, cook, batch_size, offset):
        query = ("SELECT * FROM synth_recipes WHERE wood <= %s AND smith <= %s AND gold <= %s AND cloth <= %s "
                 "AND leather <= %s AND bone <= %s AND alchemy <= %s AND cook <= %s LIMIT %s OFFSET %s")
        return self.execute_query(query, (wood, smith, gold, cloth, leather, bone, alchemy, cook, batch_size, offset), fetch_method="all")

    @db_connection_required
    def search_recipe(self, search_term, batch_size, offset):
        query = """
        SELECT * FROM (
            SELECT *, MATCH(ResultName) AGAINST(%s IN BOOLEAN MODE) AS relevance
            FROM synth_recipes
        ) AS ranked
        WHERE ranked.relevance > 0
        ORDER BY relevance DESC, ID ASC
        LIMIT %s OFFSET %s;
        """
        return self.execute_query(query, (search_term, batch_size, offset), fetch_method="all")

    @db_connection_required
    def get_regional_vendor(self, npc_id):
        query = "SELECT * FROM regional_vendors WHERE npcid=%s"
        return self.execute_query(query, (npc_id,), fetch_method="one")

    @db_connection_required
    def get_vendor_items(self, item_id):
        query = "SELECT * FROM vendor_items WHERE itemid=%s"
        return self.execute_query(query, (item_id,), fetch_method="all")

    @db_connection_required
    def get_vendor_location(self, npc_id):
        query = "SELECT * FROM vendor_locations WHERE npcid=%s"
        return self.execute_query(query, (npc_id,), fetch_method="one")


class DatabaseException(Exception):
    pass
