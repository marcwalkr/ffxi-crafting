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

        if host == "" or user == "" or password == "" or database == "":
            warnings.warn("Database configuration is incomplete")

        if cls._pool is None:
            with cls._pool_lock:
                if cls._pool is None:  # Double-checked locking
                    cls._pool = pooling.MySQLConnectionPool(
                        pool_name="mypool",
                        pool_size=20,
                        host=SettingsManager.get_database_host(),
                        user=SettingsManager.get_database_user(),
                        password=SettingsManager.get_database_password(),
                        database=SettingsManager.get_database_name()
                    )

    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def _connect(self):
        if self.connection is None:
            if self._pool is None:
                self.initialize_pool()
            self.connection = self._pool.get_connection()
            self.cursor = self.connection.cursor(buffered=True)

    def close(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def get_auction_items(self, item_id):
        self._connect()
        self.cursor.execute("SELECT * FROM auction_items WHERE itemid=%s AND no_sale=0", (item_id,))
        return self.cursor.fetchall()

    def update_auction_item(self, item_id, avg_price, sell_freq, is_stack):
        self._connect()
        self.cursor.execute(
            "UPDATE auction_items SET avg_price = %s, sell_freq = %s, new_data = 0 "
            "WHERE itemid = %s AND is_stack = %s",
            (avg_price, sell_freq, item_id, is_stack)
        )
        self.commit()

    def get_latest_sales_history(self, item_id, is_stack):
        self._connect()
        self.cursor.execute(
            "SELECT * FROM sales_history WHERE itemid=%s AND is_stack=%s AND batch_id = "
            "(SELECT MAX(batch_id) FROM sales_history WHERE itemid=%s AND is_stack=%s)",
            (item_id, is_stack, item_id, is_stack)
        )
        return self.cursor.fetchall()

    def get_guild(self, guild_id):
        self._connect()
        self.cursor.execute("SELECT * FROM guilds WHERE id=%s", (guild_id,))
        return self.cursor.fetchone()

    def get_guild_shops(self, item_id):
        self._connect()
        self.cursor.execute("SELECT * FROM guild_shops WHERE itemid=%s", (item_id,))
        return self.cursor.fetchall()

    def get_item(self, item_id):
        self._connect()
        self.cursor.execute("SELECT * FROM item_basic WHERE itemid=%s", (item_id,))
        return self.cursor.fetchone()

    def get_items(self, item_ids):
        self._connect()
        format_strings = ','.join(['%s'] * len(item_ids))
        self.cursor.execute(f"SELECT * FROM item_basic WHERE itemid IN ({format_strings})", tuple(item_ids))
        return self.cursor.fetchall()

    def get_npc_by_name(self, name):
        self._connect()
        self.cursor.execute("SELECT * FROM npc_list WHERE polutils_name=%s", (name,))
        return self.cursor.fetchone()

    def get_regional_vendors(self):
        self._connect()
        self.cursor.execute("SELECT * FROM regional_vendors")
        return self.cursor.fetchall()

    def get_recipe(self, recipe_id):
        self._connect()
        self.cursor.execute("SELECT * FROM synth_recipes WHERE id=%s", (recipe_id,))
        return self.cursor.fetchone()

    def get_recipes_by_level(self, wood, smith, gold, cloth, leather, bone, alchemy, cook, batch_size, offset):
        self._connect()
        query = ("SELECT * FROM synth_recipes WHERE wood <= %s AND smith <= %s AND gold <= %s AND cloth <= %s "
                 "AND leather <= %s AND bone <= %s AND alchemy <= %s AND cook <= %s LIMIT %s OFFSET %s")
        self.cursor.execute(query, (wood, smith, gold, cloth, leather, bone, alchemy, cook, batch_size, offset))
        return self.cursor.fetchall()

    def search_recipe(self, search_term, batch_size, offset):
        self._connect()
        query = """
        SELECT * FROM (
            SELECT *, MATCH(ResultName) AGAINST(%s IN BOOLEAN MODE) AS relevance
            FROM synth_recipes
        ) AS ranked
        WHERE ranked.relevance > 0
        ORDER BY relevance DESC, ID ASC
        LIMIT %s OFFSET %s;
        """
        self.cursor.execute(query, (search_term, batch_size, offset))
        return self.cursor.fetchall()

    def get_vendor_items(self, item_id):
        self._connect()
        self.cursor.execute("SELECT * FROM vendor_items WHERE itemid=%s", (item_id,))
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()
