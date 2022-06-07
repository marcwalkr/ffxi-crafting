import mysql.connector


class Database:
    def __init__(self) -> None:
        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="root",
            database="ffxi"
        )
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def get_auction(self, item_id):
        self.cursor.execute("SELECT * FROM auction WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchone()

    def add_auction(self, item_id, single_price, stack_price, single_frequency,
                    stack_frequency):
        self.cursor.execute("""INSERT INTO auction (itemid, single_price, stack_price,
                            single_frequency, stack_frequency)
                            VALUES (%s,%s,%s,%s,%s)""",
                            (item_id, single_price, stack_price,
                             single_frequency, stack_frequency,))
        self.commit()

    def update_auction(self, item_id, single_price, stack_price,
                       single_frequency, stack_frequency):
        self.cursor.execute("""UPDATE auction SET single_price=%s,
                            stack_price=%s, single_frequency=%s,
                            stack_frequency=%s WHERE itemid=%s""",
                            (single_price, stack_price, single_frequency,
                             stack_frequency, item_id,))
        self.commit()

    def get_item(self, item_id):
        self.cursor.execute("SELECT * FROM item_basic WHERE itemid=%s",
                            (item_id,))
        return self.cursor.fetchone()

    def get_recipes(self, skill_set):
        # Select within 5 levels of skill
        wood = skill_set.wood + 5
        smith = skill_set.smith + 5
        gold = skill_set.gold + 5
        cloth = skill_set.cloth + 5
        leather = skill_set.leather + 5
        bone = skill_set.bone + 5
        alchemy = skill_set.alchemy + 5
        cook = skill_set.cook + 5

        self.cursor.execute("""SELECT * FROM synth_recipes WHERE Wood<=%s and
                            Smith<=%s and Gold<=%s and Cloth<=%s and
                            Leather<=%s and Bone<=%s and Alchemy<=%s and
                            Cook<=%s""", (wood, smith, gold, cloth, leather,
                                          bone, alchemy, cook,))

        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()
