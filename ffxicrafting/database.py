from sqlite3 import connect, IntegrityError
from logger import Logger


class Database:
    def __init__(self) -> None:
        self.connection = connect("crafting.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cur = self.connection.cursor()
        self.create_tables()

    def __del__(self):
        self.connection.close()

    def create_tables(self):
        self.create_items_table()
        self.create_vendors_table()
        self.create_vendor_items_table()
        self.create_auction_items_table()
        self.create_recipes_table()
        self.create_synthesis_results_table()

    def create_items_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS items (
                            name text PRIMARY KEY,
                            stack_quantity integer
                            )""")

    def create_vendors_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS vendors (
                            npc_name text PRIMARY KEY,
                            area text NOT NULL,
                            coordinates text NOT NULL,
                            type text NOT NULL
                            )""")

    def create_vendor_items_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS vendor_items (
                            item_name text,
                            vendor_name text,
                            price integer NOT NULL,
                            PRIMARY KEY (item_name, vendor_name),
                            FOREIGN KEY (item_name) REFERENCES items (name),
                            FOREIGN KEY (vendor_name) REFERENCES vendors (npc_name)
                            )""")

    def create_auction_items_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS auction_items (
                            item_id integer PRIMARY KEY,
                            item_name text,
                            single_price integer,
                            stack_price integer,
                            single_frequency real,
                            stack_frequency real,
                            FOREIGN KEY (item_name) REFERENCES items (name)
                            )""")

    def create_recipes_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS recipes (
                            id INTEGER PRIMARY KEY,
                            crystal text NOT NULL,
                            ingredient1 text NOT NULL,
                            ingredient2 text,
                            ingredient3 text,
                            ingredient4 text,
                            ingredient5 text,
                            ingredient6 text,
                            ingredient7 text,
                            ingredient8 text,
                            craft text NOT NULL,
                            skill_cap integer NOT NULL,
                            FOREIGN KEY (crystal) REFERENCES items (name),
                            FOREIGN KEY (ingredient1) REFERENCES items (name),
                            FOREIGN KEY (ingredient2) REFERENCES items (name),
                            FOREIGN KEY (ingredient3) REFERENCES items (name),
                            FOREIGN KEY (ingredient4) REFERENCES items (name),
                            FOREIGN KEY (ingredient5) REFERENCES items (name),
                            FOREIGN KEY (ingredient6) REFERENCES items (name),
                            FOREIGN KEY (ingredient7) REFERENCES items (name),
                            FOREIGN KEY (ingredient8) REFERENCES items (name),
                            UNIQUE (crystal, ingredient1, ingredient2,
                                    ingredient3, ingredient4, ingredient5,
                                    ingredient6, ingredient7, ingredient8)
                            )""")

    def create_synthesis_results_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS synthesis_results (
                            item_name text NOT NULL,
                            recipe_id integer NOT NULL,
                            quantity integer NOT NULL,
                            quality_level text NOT NULL,
                            PRIMARY KEY (recipe_id, quality_level),
                            FOREIGN KEY (item_name) REFERENCES items (name),
                            FOREIGN KEY (recipe_id) REFERENCES synthesis_recipes (id)
                            )""")

    def get_item(self, name):
        self.cur.execute("SELECT * FROM items WHERE name=?", (name,))
        return self.cur.fetchone()

    def add_item(self, item):
        self.cur.execute("""INSERT INTO items VALUES (:name,
                         :stack_quantity)""",
                         {"name": item.name,
                          "stack_quantity": item.stack_quantity
                          })
        self.commit()
        Logger.print_green("Added item \"{}\"".format(item.name))

    def remove_item(self, name):
        try:
            self.cur.execute("DELETE FROM items WHERE name=?", (name,))
            Logger.print_green("Removed item \"{}\"".format(name))
        except IntegrityError as e:
            Logger.print_red(str(e))

        self.commit()

    def get_vendor(self, npc_name):
        self.cur.execute("SELECT * FROM vendors WHERE npc_name=?", (npc_name,))
        return self.cur.fetchone()

    def add_vendor(self, vendor):
        self.cur.execute("""INSERT INTO vendors VALUES (:npc_name, :area,
                            :coordinates, :type)""",
                         {"npc_name": vendor.npc_name,
                          "area": vendor.area,
                          "coordinates": vendor.coordinates,
                          "type": vendor.vendor_type
                          })
        self.commit()
        Logger.print_green("Added vendor \"{}\"".format(vendor.npc_name))

    def remove_vendor(self, npc_name):
        try:
            self.cur.execute("DELETE FROM vendors WHERE npc_name=?",
                             (npc_name,))
            Logger.print_green("Removed vendor \"{}\"".format(npc_name))
        except IntegrityError as e:
            Logger.print_red(str(e))

        self.commit()

    def get_vendor_item(self, item_name, vendor_name):
        self.cur.execute("""SELECT * FROM vendor_items WHERE item_name=? and
                         vendor_name=?""", (item_name, vendor_name,))
        return self.cur.fetchone()

    def add_vendor_item(self, vendor_item):
        item_name = vendor_item.item_name
        vendor_name = vendor_item.vendor_name
        price = vendor_item.price

        try:
            self.cur.execute("""INSERT INTO vendor_items VALUES (:item_name,
                                :vendor_name, :price)""",
                             {"item_name": item_name,
                              "vendor_name": vendor_name,
                              "price": price
                              })
            Logger.print_green("Added vendor item \"{}\"".format(item_name) +
                               " sold by \"{}\"".format(vendor_name))
        except IntegrityError as e:
            Logger.print_red(str(e))

        self.commit()

    def remove_vendor_item(self, item_name, vendor_name):
        self.cur.execute("""DELETE FROM vendor_items WHERE item_name=? and
                         vendor_name=?""", (item_name, vendor_name,))
        self.commit()
        Logger.print_green("Removed vendor item \"{}\" sold by \"{}\""
                           .format(item_name, vendor_name))

    def get_auction_item(self, item_name):
        self.cur.execute("""SELECT * FROM auction_items
                         WHERE item_name=?""", (item_name,))
        return self.cur.fetchone()

    def get_all_auction_items(self):
        self.cur.execute("SELECT * FROM auction_items")
        return self.cur.fetchall()

    def add_auction_item(self, auction_item):
        self.cur.execute("""INSERT INTO auction_items VALUES (:item_id,
                         :item_name, :single_price, :stack_price,
                         :single_frequency, :stack_frequency)""",
                         {"item_id": auction_item.item_id,
                          "item_name": auction_item.item_name,
                          "single_price": auction_item.single_price,
                          "stack_price": auction_item.stack_price,
                          "single_frequency": auction_item.single_frequency,
                          "stack_frequency": auction_item.stack_frequency
                          })

        self.commit()
        Logger.print_green("Added auction item \"{}\""
                           .format(auction_item.item_name))

    def remove_auction_item(self, item_name):
        self.cur.execute("DELETE FROM auction_items WHERE item_name=?",
                         (item_name,))
        self.commit()
        Logger.print_green("Removed auction item \"{}\"".format(item_name))

    def update_auction_item(self, auction_item):
        self.cur.execute("""UPDATE auction_items SET single_price=?,
                         stack_price=?, single_frequency=?, stack_frequency=?
                         WHERE item_id=?""", (auction_item.single_price,
                                              auction_item.stack_price,
                                              auction_item.single_frequency,
                                              auction_item.stack_frequency,
                                              auction_item.item_id,))
        self.commit()
        Logger.print_green("Updated prices and frequencies for \"{}\""
                           .format(auction_item.item_name))

    def commit(self):
        self.connection.commit()

    # def get_all_items(self):
    #     self.cur.execute("SELECT * FROM items")
    #     return self.cur.fetchall()

    # def update_item_vendor_price(self, name, vendor_price):
    #     self.cur.execute("""UPDATE items
    #                         SET vendor_price=?
    #                         WHERE name=?""", (vendor_price, name,))
    #     self.commit()

    # def add_recipe(self, recipe):
    #     ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, \
    #         ingredient6, ingredient7, ingredient8 = recipe.ingredients

    #     self.cur.execute("""INSERT INTO recipes VALUES (:name, :crystal,
    #                             :ingredient1, :ingredient2, :ingredient3,
    #                             :ingredient4, :ingredient5, :ingredient6,
    #                             :ingredient7, :ingredient8, :nq_yield,
    #                             :hq1_yield, :hq2_yield, :hq3_yield, :craft,
    #                             :skill_cap, :synth_cost)""",
    #                      {"name": recipe.name,
    #                       "crystal": recipe.crystal,
    #                       "ingredient1": ingredient1,
    #                       "ingredient2": ingredient2,
    #                       "ingredient3": ingredient3,
    #                       "ingredient4": ingredient4,
    #                       "ingredient5": ingredient5,
    #                       "ingredient6": ingredient6,
    #                       "ingredient7": ingredient7,
    #                       "ingredient8": ingredient8,
    #                       "nq_yield": recipe.nq_yield,
    #                       "hq1_yield": recipe.hq1_yield,
    #                       "hq2_yield": recipe.hq2_yield,
    #                       "hq3_yield": recipe.hq3_yield,
    #                       "craft": recipe.craft,
    #                       "skill_cap": recipe.skill_cap,
    #                       "synth_cost": recipe.synth_cost
    #                       })
    #     self.commit()

    # def get_recipes(self, name):
    #     self.cur.execute("SELECT * FROM recipes WHERE name=?", (name,))
    #     return self.cur.fetchall()

    # def get_all_recipes(self):
    #     self.cur.execute("SELECT * FROM recipes")
    #     return self.cur.fetchall()

    # def remove_recipe(self, name, crystal, ingredients):
    #     empty_slots = 8 - len(ingredients)
    #     full_ingredients = add_nones(ingredients, empty_slots)

    #     query_string = "DELETE FROM recipes WHERE name=? and crystal=? "

    #     for i, ingredient in enumerate(full_ingredients, start=1):
    #         if ingredient is None:
    #             append_str = " and ingredient{} IS NULL".format(str(i))
    #             query_string += append_str
    #         else:
    #             append_str = " and ingredient{}=?".format(str(i))
    #             query_string += append_str

    #     self.cur.execute(query_string, (name, crystal, *ingredients))
    #     self.commit()

    # def update_recipe_synth_cost(self, name, new_cost):
    #     self.cur.execute("""UPDATE recipes
    #                         SET synth_cost=?
    #                         WHERE name=?""", (new_cost, name,))
    #     self.commit()

    # def recipe_is_in_database(self, name, crystal, ingredients):
    #     recipe_tuples = self.get_recipes(name)
    #     for recipe_tuple in recipe_tuples:
    #         tuple_name, tuple_crystal = recipe_tuple[0:2]
    #         tuple_ingredients = recipe_tuple[2:10]
    #         tuple_ingredients = remove_nones(tuple_ingredients)

    #         same_recipe = tuple_name == name and tuple_crystal == crystal and \
    #             same_elements(tuple_ingredients, ingredients)

    #         if same_recipe:
    #             return True

    #     return False
