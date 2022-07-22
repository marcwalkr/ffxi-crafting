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

    def get_auction(self, item_id):
        self.cursor.execute("SELECT * FROM auction WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchone()

    def add_auction(self, item_id, single_sales, single_price_sum, stack_sales,
                    stack_price_sum, days):
        self.cursor.execute("""INSERT INTO auction (itemid, single_sales,
                            single_price_sum, stack_sales, stack_price_sum,
                            days)
                            VALUES (%s,%s,%s,%s,%s,%s)""",
                            (item_id, single_sales, single_price_sum,
                             stack_sales, stack_price_sum, days,))
        self.commit()

    def update_auction(self, item_id, single_sales, single_price_sum,
                       stack_sales, stack_price_sum, days, timestamp):
        self.cursor.execute("""UPDATE auction SET single_sales=single_sales+%s,
                            single_price_sum=single_price_sum+%s,
                            stack_sales=stack_sales+%s,
                            stack_price_sum=stack_price_sum+%s, days=days+%s,
                            last_updated=%s WHERE itemid=%s""",
                            (single_sales, single_price_sum, stack_sales,
                             stack_price_sum, days, timestamp, item_id,))
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

    def get_recipes(self, skill_set, skill_range):
        wood = skill_set.wood + skill_range
        smith = skill_set.smith + skill_range
        gold = skill_set.gold + skill_range
        cloth = skill_set.cloth + skill_range
        leather = skill_set.leather + skill_range
        bone = skill_set.bone + skill_range
        alchemy = skill_set.alchemy + skill_range
        cook = skill_set.cook + skill_range

        self.cursor.execute("""SELECT * FROM synth_recipes WHERE Wood<=%s and
                            Smith<=%s and Gold<=%s and Cloth<=%s and
                            Leather<=%s and Bone<=%s and Alchemy<=%s and
                            Cook<=%s""", (wood, smith, gold, cloth, leather,
                                          bone, alchemy, cook,))

        return self.cursor.fetchall()

    def get_vendor_items(self, item_id):
        self.cursor.execute("SELECT * FROM vendor_items WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchall()

    def get_all_vendor_items(self):
        self.cursor.execute("SELECT * FROM vendor_items")
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
