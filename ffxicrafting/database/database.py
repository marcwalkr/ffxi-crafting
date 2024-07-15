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

    def add_auction_item(self, item_id, single_price, stack_price):
        self.cursor.execute("INSERT INTO auction_items VALUES (%s, %s, %s)",
                            (item_id, single_price, stack_price,))
        self.commit()

    def update_auction_item(self, item_id, single_price, stack_price):
        self.cursor.execute("UPDATE auction_items SET single_price = %s, stack_price = %s WHERE itemid = %s",
                            (single_price, stack_price, item_id))
        self.commit()

    def delete_auction_items(self):
        self.cursor.execute("DELETE FROM auction_items")
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

    def get_regional_vendors(self):
        self.cursor.execute("SELECT * FROM regional_vendors")
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()
