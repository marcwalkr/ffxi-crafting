import threading
import logging
from mysql.connector import pooling
from config.settings_manager import SettingsManager

logger = logging.getLogger(__name__)


class Database:
    pool = None
    pool_lock = threading.Lock()
    local = threading.local()

    @classmethod
    def initialize_pool(cls):
        with cls.pool_lock:
            if cls.pool is None:
                config = {
                    "host": SettingsManager.get_database_host(),
                    "user": SettingsManager.get_database_user(),
                    "password": SettingsManager.get_database_password(),
                    "database": SettingsManager.get_database_name()
                }

                if not all(config.values()):
                    logger.error("Database configuration is incomplete")
                    return

                cls.pool = pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=32,
                    **config
                )

    @classmethod
    def get_connection(cls):
        if not hasattr(cls.local, "connection") or cls.local.connection is None:
            cls.initialize_pool()
            cls.local.connection = cls.pool.get_connection()
            cls.local.cursor = cls.local.connection.cursor(buffered=True)
        return cls.local.connection, cls.local.cursor

    @classmethod
    def close_connection(cls):
        if hasattr(cls.local, "connection") and cls.local.connection is not None:
            cls.local.cursor.close()
            cls.local.connection.close()
            cls.local.connection = None
            cls.local.cursor = None

    def execute_query(self, query, params=None, fetch_one=False, commit=False):
        connection, cursor = self.get_connection()

        try:
            cursor.execute(query, params)
            if commit:
                connection.commit()
                return None
            if fetch_one:
                return cursor.fetchone()
            return cursor.fetchall() or []
        except Exception as e:
            if commit:
                connection.rollback()
            logger.error(f"Database query failed: {e}")
            return None

    def get_auction_items(self, item_id):
        query = "SELECT * FROM auction_items WHERE itemid=%s AND no_sale=0"
        return self.execute_query(query, (item_id,), fetch_one=False)

    def update_auction_item(self, item_id, avg_price, sell_freq, is_stack):
        query = "UPDATE auction_items SET avg_price = %s, sell_freq = %s, new_data = 0 "
        query += "WHERE itemid = %s AND is_stack = %s"
        return self.execute_query(query, (avg_price, sell_freq, item_id, is_stack), commit=True)

    def get_latest_sales_history(self, item_id, is_stack):
        query = "SELECT * FROM sales_history WHERE itemid=%s AND is_stack=%s AND batch_id = "
        query += "(SELECT MAX(batch_id) FROM sales_history WHERE itemid=%s AND is_stack=%s)"
        return self.execute_query(query, (item_id, is_stack, item_id, is_stack), fetch_one=False)

    def get_guild_shops(self, item_id):
        query = "SELECT * FROM guild_shops WHERE itemid=%s"
        return self.execute_query(query, (item_id,), fetch_one=False)

    def get_guild_vendor(self, guild_id):
        query = "SELECT * FROM guild_vendors WHERE guildid=%s"
        return self.execute_query(query, (guild_id,), fetch_one=True)

    def get_item(self, item_id):
        query = "SELECT * FROM item_basic WHERE itemid=%s"
        return self.execute_query(query, (item_id,), fetch_one=True)

    def get_items(self, item_ids):
        format_strings = ','.join(['%s'] * len(item_ids))
        query = f"SELECT * FROM item_basic WHERE itemid IN ({format_strings})"
        return self.execute_query(query, tuple(item_ids), fetch_one=False)

    def get_npc(self, npc_id):
        query = "SELECT * FROM npc_list WHERE npcid=%s"
        return self.execute_query(query, (npc_id,), fetch_one=True)

    def get_recipe(self, recipe_id):
        query = "SELECT * FROM synth_recipes WHERE id=%s"
        return self.execute_query(query, (recipe_id,), fetch_one=True)

    def get_recipes_by_level(self, wood, smith, gold, cloth, leather, bone, alchemy, cook, batch_size, offset):
        query = ("SELECT * FROM synth_recipes WHERE wood <= %s AND smith <= %s AND gold <= %s AND cloth <= %s "
                 "AND leather <= %s AND bone <= %s AND alchemy <= %s AND cook <= %s LIMIT %s OFFSET %s")
        return self.execute_query(query, (wood, smith, gold, cloth, leather, bone, alchemy, cook, batch_size, offset), fetch_one=False)

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
        return self.execute_query(query, (search_term, batch_size, offset), fetch_one=False)

    def get_all_result_item_ids(self):
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
        results = self.execute_query(query, (), fetch_one=False)
        return [result[0] for result in results]

    def get_regional_vendor(self, npc_id):
        query = "SELECT * FROM regional_vendors WHERE npcid=%s"
        return self.execute_query(query, (npc_id,), fetch_one=True)

    def get_vendor_items(self, item_id):
        query = "SELECT * FROM vendor_items WHERE itemid=%s"
        return self.execute_query(query, (item_id,), fetch_one=False)

    def get_vendor_location(self, npc_id):
        query = "SELECT * FROM vendor_locations WHERE npcid=%s"
        return self.execute_query(query, (npc_id,), fetch_one=True)
