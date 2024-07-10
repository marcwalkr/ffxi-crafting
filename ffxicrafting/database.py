import mysql.connector


class Database:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="ffxi"
        )
        self.cursor = self.connection.cursor(buffered=True)

    def __del__(self):
        self.connection.close()

    def get_auction_item(self, item_id):
        self.cursor.execute("SELECT * FROM auction_items WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchone()

    def add_auction_item(self, item_id, avg_single_price, avg_stack_price, sales_frequency):
        query = """
                INSERT INTO auction_items (itemid, avg_single_price, avg_stack_price, sales_frequency)
                VALUES (%s, %s, %s, %s)
                """
        self.cursor.execute(query, (item_id, avg_single_price, avg_stack_price, sales_frequency))
        self.commit()

    def update_auction_item(self, item_id, avg_single_price, avg_stack_price, sales_frequency):
        query = """
                UPDATE auction_items
                SET avg_single_price = %s, avg_stack_price = %s, sales_frequency = %s
                WHERE itemid = %s
                """
        self.cursor.execute(query, (avg_single_price, avg_stack_price, sales_frequency, item_id,))
        self.commit()

    def delete_auction_items(self):
        self.cursor.execute("DELETE FROM auction_items")
        self.commit()

    def get_guild_shops(self, item_id):
        self.cursor.execute("SELECT * FROM guild_shops WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchall()

    def get_item(self, item_id):
        self.cursor.execute("SELECT * FROM item_basic WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchone()

    def get_item_by_name(self, item_name):
        self.cursor.execute("SELECT * FROM item_basic WHERE name=%s",
                            (item_name,))
        return self.cursor.fetchone()

    def get_npc(self, npc_id):
        self.cursor.execute("SELECT * FROM npc_list WHERE npcid=%s", (npc_id,))
        return self.cursor.fetchone()

    def get_npc_by_name(self, name):
        self.cursor.execute("SELECT * FROM npc_list WHERE polutils_name=%s",
                            (name,))
        return self.cursor.fetchone()

    def get_recipe(self, recipe_id):
        self.cursor.execute("SELECT * FROM synth_recipes WHERE id=%s",
                            (recipe_id,))
        return self.cursor.fetchone()

    def get_all_recipes(self):
        self.cursor.execute("SELECT * FROM synth_recipes")
        return self.cursor.fetchall()

    def get_vendor_items(self, item_id):
        self.cursor.execute("SELECT * FROM vendor_items WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchall()

    def get_regional_vendors(self):
        self.cursor.execute("SELECT * FROM regional_vendors")
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()
