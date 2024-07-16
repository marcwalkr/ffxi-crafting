import mysql.connector
from dotenv import load_dotenv
import os


class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            passwd=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        self.cursor = self.connection.cursor(buffered=True)

    def __del__(self):
        self.connection.close()

    def get_auction_item(self, item_id, is_stack):
        self.cursor.execute("SELECT * FROM auction_items WHERE itemid=%s AND is_stack=%s AND no_sale=0",
                            (item_id, is_stack))
        return self.cursor.fetchone()

    def update_auction_item(self, item_id, avg_price, num_sales, sell_freq, is_stack):
        self.cursor.execute(
            "UPDATE auction_items SET avg_price = %s, num_sales = %s, sell_freq = %s, new_data = 0 "
            "WHERE itemid = %s AND is_stack = %s",
            (avg_price, num_sales, sell_freq, item_id, is_stack)
        )
        self.commit()

    def get_guild(self, guild_id):
        self.cursor.execute("SELECT * FROM guilds WHERE id=%s", (guild_id,))
        return self.cursor.fetchone()

    def get_guild_shops(self, item_id):
        self.cursor.execute("SELECT * FROM guild_shops WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchall()

    def get_item(self, item_id):
        self.cursor.execute("SELECT * FROM item_basic WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchone()

    def get_npc_by_name(self, name):
        self.cursor.execute("SELECT * FROM npc_list WHERE polutils_name=%s",
                            (name,))
        return self.cursor.fetchone()

    def get_regional_vendors(self):
        self.cursor.execute("SELECT * FROM regional_vendors")
        return self.cursor.fetchall()

    def get_latest_sales_history(self, item_id, is_stack):
        self.cursor.execute(
            "SELECT * FROM sales_history WHERE itemid=%s AND is_stack=%s AND batch_id = "
            "(SELECT MAX(batch_id) FROM sales_history WHERE itemid=%s AND is_stack=%s)",
            (item_id, is_stack, item_id, is_stack)
        )
        return self.cursor.fetchall()

    def get_recipe(self, recipe_id):
        self.cursor.execute("SELECT * FROM synth_recipes WHERE id=%s",
                            (recipe_id,))
        return self.cursor.fetchone()

    def get_recipes_by_craft_levels(self, wood, smith, gold, cloth, leather, bone, alchemy, cook):
        query = ("SELECT * FROM synth_recipes WHERE wood <= %s AND smith <= %s AND gold <= %s AND cloth <= %s "
                 "AND leather <= %s AND bone <= %s AND alchemy <= %s AND cook <= %s")
        self.cursor.execute(query, (wood, smith, gold, cloth, leather, bone, alchemy, cook))
        return self.cursor.fetchall()

    def search_recipe(self, search_term):
        self.cursor.execute("SELECT * FROM synth_recipes WHERE ResultName LIKE %s", ("%" + search_term + "%",))
        return self.cursor.fetchall()

    def get_vendor_items(self, item_id):
        self.cursor.execute("SELECT * FROM vendor_items WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()
