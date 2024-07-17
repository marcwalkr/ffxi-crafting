from mysql.connector import pooling
from dotenv import load_dotenv
import os


class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.pool = None
        self.active_connections = []

    def get_pool(self):
        if self.pool is None:
            self.pool = self.create_pool()
        return self.pool

    def create_pool(self):
        return pooling.MySQLConnectionPool(
            pool_name="pool",
            pool_size=10,
            pool_reset_session=True,
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

    def get_connection(self):
        connection = self.get_pool().get_connection()
        self.active_connections.append(connection)
        return connection

    def close_connection(self, connection):
        if connection.is_connected():
            connection.close()
        if connection in self.active_connections:
            self.active_connections.remove(connection)

    def close_all_connections(self):
        for connection in self.active_connections:
            if connection.is_connected():
                connection.close()
        self.active_connections.clear()

    def get_auction_item(self, item_id, is_stack):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM auction_items WHERE itemid=%s AND is_stack=%s AND no_sale=0",
                       (item_id, is_stack))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection(connection)
        return result

    def update_auction_item(self, item_id, avg_price, num_sales, sell_freq, is_stack):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE auction_items SET avg_price = %s, num_sales = %s, sell_freq = %s, new_data = 0 "
            "WHERE itemid = %s AND is_stack = %s",
            (avg_price, num_sales, sell_freq, item_id, is_stack)
        )
        connection.commit()
        cursor.close()
        self.close_connection(connection)

    def get_latest_sales_history(self, item_id, is_stack):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute(
            "SELECT * FROM sales_history WHERE itemid=%s AND is_stack=%s AND batch_id = "
            "(SELECT MAX(batch_id) FROM sales_history WHERE itemid=%s AND is_stack=%s)",
            (item_id, is_stack, item_id, is_stack)
        )
        result = cursor.fetchall()
        cursor.close()
        self.close_connection(connection)
        return result

    def get_guild(self, guild_id):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM guilds WHERE id=%s", (guild_id,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection(connection)
        return result

    def get_guild_shops(self, item_id):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM guild_shops WHERE itemid=%s", (item_id,))
        result = cursor.fetchall()
        cursor.close()
        self.close_connection(connection)
        return result

    def get_item(self, item_id):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM item_basic WHERE itemid=%s", (item_id,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection(connection)
        return result

    def get_npc_by_name(self, name):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM npc_list WHERE polutils_name=%s", (name,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection(connection)
        return result

    def get_regional_vendors(self):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM regional_vendors")
        result = cursor.fetchall()
        cursor.close()
        self.close_connection(connection)
        return result

    def get_recipe(self, recipe_id):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM synth_recipes WHERE id=%s", (recipe_id,))
        result = cursor.fetchone()
        cursor.close()
        self.close_connection(connection)
        return result

    def get_recipes_by_level_generator(self, wood, smith, gold, cloth, leather, bone, alchemy, cook):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        query = ("SELECT * FROM synth_recipes WHERE wood <= %s AND smith <= %s AND gold <= %s AND cloth <= %s "
                 "AND leather <= %s AND bone <= %s AND alchemy <= %s AND cook <= %s")
        cursor.execute(query, (wood, smith, gold, cloth, leather, bone, alchemy, cook))
        for row in cursor:
            yield row
        cursor.close()
        self.close_connection(connection)

    def search_recipe_generator(self, search_term):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM synth_recipes WHERE ResultName LIKE %s", ("%" + search_term + "%",))
        for row in cursor:
            yield row
        cursor.close()
        self.close_connection(connection)

    def get_vendor_items(self, item_id):
        connection = self.get_connection()
        cursor = connection.cursor(buffered=True)
        cursor.execute("SELECT * FROM vendor_items WHERE itemid=%s", (item_id,))
        result = cursor.fetchall()
        cursor.close()
        self.close_connection(connection)
        return result

    def commit(self):
        connection = self.get_connection()
        connection.commit()
        self.close_connection(connection)
