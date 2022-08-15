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

    def get_auction_pages(self, item_id):
        self.cursor.execute("SELECT * FROM auction_pages WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchall()

    def get_all_auction_pages(self):
        self.cursor.execute("SELECT * FROM auction_pages")
        return self.cursor.fetchall()

    def add_auction_page(self, item_id, single_sales, single_price_sum,
                         stack_sales, stack_price_sum, num_days, accessed):
        self.cursor.execute("""INSERT INTO auction_pages (itemid, single_sales,
                            single_price_sum, stack_sales, stack_price_sum,
                            num_days, accessed)
                            VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                            (item_id, single_sales, single_price_sum,
                             stack_sales, stack_price_sum, num_days,
                             accessed,))
        self.commit()

    def delete_auction_pages_older_than(self, days):
        self.cursor.execute("""DELETE FROM auction_pages WHERE
                            DATEDIFF(UTC_TIMESTAMP(), accessed) > %s""",
                            (days,))
        self.commit()

    def get_guild_shops(self, item_id):
        self.cursor.execute("SELECT * FROM guild_shops WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchall()

    def get_guild(self, guild_id):
        self.cursor.execute("SELECT * FROM guilds WHERE guildid=%s",
                            (guild_id,))
        return self.cursor.fetchone()

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

    def add_vendor_item(self, item_id, npc_id, price):
        try:
            self.cursor.execute("""INSERT INTO vendor_items (itemid, npcid, price)
                                VALUES (%s,%s,%s)""", (item_id, npc_id, price,))
        except mysql.connector.errors.IntegrityError:
            pass

        self.commit()

    def commit(self):
        self.connection.commit()
