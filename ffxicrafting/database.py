import sqlite3
from colorama import Fore, init
from helpers import remove_nones, same_elements, add_nones

# Auto reset style with colorama
init(autoreset=True)


class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect("crafting.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.cur = self.connection.cursor()
        self.create_tables()

    def __del__(self):
        self.connection.close()

    def create_tables(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS items (
                            name text PRIMARY KEY NOT NULL,
                            stack_quantity integer,
                            vendor_price integer
                            )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS recipes (
                            name text NOT NULL,
                            crystal text NOT NULL,
                            ingredient1 text NOT NULL,
                            ingredient2 text,
                            ingredient3 text,
                            ingredient4 text,
                            ingredient5 text,
                            ingredient6 text,
                            ingredient7 text,
                            ingredient8 text,
                            synth_yield integer NOT NULL,
                            synth_cost real NOT NULL,
                            FOREIGN KEY (name) REFERENCES items (name),
                            FOREIGN KEY (crystal) REFERENCES items (name),
                            FOREIGN KEY (ingredient1) REFERENCES items (name),
                            FOREIGN KEY (ingredient2) REFERENCES items (name),
                            FOREIGN KEY (ingredient3) REFERENCES items (name),
                            FOREIGN KEY (ingredient4) REFERENCES items (name),
                            FOREIGN KEY (ingredient5) REFERENCES items (name),
                            FOREIGN KEY (ingredient6) REFERENCES items (name),
                            FOREIGN KEY (ingredient7) REFERENCES items (name),
                            FOREIGN KEY (ingredient8) REFERENCES items (name)
                            )""")

        self.cur.execute("""CREATE TABLE IF NOT EXISTS auction_listings (
                            name text NOT NULL,
                            quantity integer NOT NULL,
                            price integer NOT NULL,
                            sell_freq real NOT NULL,
                            PRIMARY KEY (name, quantity),
                            FOREIGN KEY (name) REFERENCES items (name)
                            )""")

    def add_item(self, item):
        self.cur.execute("""INSERT INTO items VALUES (:name, :stack_quantity,
                         :vendor_price)""",
                         {"name": item.name,
                          "stack_quantity": item.stack_quantity,
                          "vendor_price": item.vendor_price
                          })
        self.commit()

    def get_item(self, name):
        self.cur.execute("SELECT * FROM items WHERE name=?", (name,))
        return self.cur.fetchone()

    def get_all_items(self):
        self.cur.execute("SELECT * FROM items")
        return self.cur.fetchall()

    def remove_item(self, name):
        try:
            self.cur.execute("DELETE FROM items WHERE name=?", (name,))
            self.commit()
        except sqlite3.IntegrityError:
            print(Fore.RED + "Failed to remove item: a recipe or auction " +
                  "listing references it")

    def update_item_vendor_price(self, name, vendor_price):
        self.cur.execute("""UPDATE items
                            SET vendor_price=?
                            WHERE name=?""", (vendor_price, name,))
        self.commit()

    def item_is_in_database(self, name):
        item = self.get_item(name)
        return item is not None

    def add_recipe(self, recipe):
        ingredient1, ingredient2, ingredient3, ingredient4, ingredient5, \
            ingredient6, ingredient7, ingredient8 = recipe.ingredients

        try:
            self.cur.execute("""INSERT INTO recipes VALUES (:name, :crystal,
                                :ingredient1, :ingredient2, :ingredient3,
                                :ingredient4, :ingredient5, :ingredient6,
                                :ingredient7, :ingredient8, :synth_yield,
                                :synth_cost)""",
                             {"name": recipe.name,
                              "crystal": recipe.crystal,
                              "ingredient1": ingredient1,
                              "ingredient2": ingredient2,
                              "ingredient3": ingredient3,
                              "ingredient4": ingredient4,
                              "ingredient5": ingredient5,
                              "ingredient6": ingredient6,
                              "ingredient7": ingredient7,
                              "ingredient8": ingredient8,
                              "synth_yield": recipe.synth_yield,
                              "synth_cost": recipe.synth_cost
                              })
            self.commit()
        except sqlite3.IntegrityError:
            raise ValueError(Fore.RED + "Failed to add recipe: a necessary " +
                             "item was not found or the recipe already exists")

    def get_recipes(self, name):
        self.cur.execute("SELECT * FROM recipes WHERE name=?", (name,))
        return self.cur.fetchall()

    def get_all_recipes(self):
        self.cur.execute("SELECT * FROM recipes")
        return self.cur.fetchall()

    def remove_recipe(self, name, crystal, ingredients):
        empty_slots = 8 - len(ingredients)
        full_ingredients = add_nones(ingredients, empty_slots)

        query_string = "DELETE FROM recipes WHERE name=? and crystal=? "

        for i, ingredient in enumerate(full_ingredients, start=1):
            if ingredient is None:
                append_str = " and ingredient{} IS NULL".format(str(i))
                query_string += append_str
            else:
                append_str = " and ingredient{}=?".format(str(i))
                query_string += append_str

        self.cur.execute(query_string, (name, crystal, *ingredients))
        self.commit()

    def update_recipe_synth_cost(self, name, new_cost):
        self.cur.execute("""UPDATE recipes
                            SET synth_cost=?
                            WHERE name=?""", (new_cost, name,))
        self.commit()

    def recipe_is_in_database(self, name, crystal, ingredients):
        recipe_tuples = self.get_recipes(name)
        for recipe_tuple in recipe_tuples:
            tuple_name, tuple_crystal = recipe_tuple[0:2]
            tuple_ingredients = recipe_tuple[2:10]
            tuple_ingredients = remove_nones(tuple_ingredients)

            same_recipe = tuple_name == name and tuple_crystal == crystal and \
                same_elements(tuple_ingredients, ingredients)

            if same_recipe:
                return True

        return False

    def add_auction_listing(self, auction_listing):
        self.cur.execute("""INSERT INTO auction_listings VALUES (:name,
                         :quantity, :price, :sell_freq)""",
                         {"name": auction_listing.name,
                          "quantity": auction_listing.quantity,
                          "price": auction_listing.price,
                          "sell_freq": auction_listing.sell_freq
                          })
        self.commit()

    def get_auction_listings(self, name):
        self.cur.execute("""SELECT * FROM auction_listings
                         WHERE name=?""", (name,))
        return self.cur.fetchall()

    def get_all_auction_listings(self):
        self.cur.execute("SELECT * FROM auction_listings")
        return self.cur.fetchall()

    def remove_auction_listings(self, name):
        self.cur.execute("DELETE FROM auction_listings WHERE name=?", (name,))
        self.commit()

    def update_auction_listing_price(self, name, new_price):
        self.cur.execute("""UPDATE auction_listings
                            SET price=?
                            WHERE name=?""", (new_price, name,))
        self.commit()

    def update_auction_listing_sell_freq(self, name, new_freq):
        self.cur.execute("""UPDATE auction_listings
                            SET sell_freq=?
                            WHERE name=?""", (new_freq, name,))
        self.commit()

    def delete_all_auction_listings(self):
        self.cur.execute("DELETE FROM auction_listings")
        self.commit()

    def commit(self):
        self.connection.commit()

    def recreate_items_table(self):
        self.connection.execute("PRAGMA foreign_keys = 0")

        self.cur.execute("""CREATE TABLE items_temp (
                            name text PRIMARY KEY NOT NULL,
                            stack_quantity integer,
                            vendor_price integer
                            )""")

        self.cur.execute("""INSERT INTO items_temp (name, stack_quantity,
                         vendor_price)
                         SELECT name, stack_quantity, vendor_price
                         FROM items""")
        self.commit()

        self.cur.execute("DROP TABLE items")

        self.cur.execute("ALTER TABLE items_temp RENAME TO items")

        self.connection.execute("PRAGMA foreign_keys = 1")

    def recreate_recipes_table(self):
        self.connection.execute("PRAGMA foreign_keys = 0")

        self.cur.execute("""CREATE TABLE recipes_temp (
                            name text NOT NULL,
                            crystal text NOT NULL,
                            ingredient1 text NOT NULL,
                            ingredient2 text,
                            ingredient3 text,
                            ingredient4 text,
                            ingredient5 text,
                            ingredient6 text,
                            ingredient7 text,
                            ingredient8 text,
                            synth_yield integer NOT NULL,
                            synth_cost real NOT NULL,
                            FOREIGN KEY (name) REFERENCES items (name),
                            FOREIGN KEY (crystal) REFERENCES items (name),
                            FOREIGN KEY (ingredient1) REFERENCES items (name),
                            FOREIGN KEY (ingredient2) REFERENCES items (name),
                            FOREIGN KEY (ingredient3) REFERENCES items (name),
                            FOREIGN KEY (ingredient4) REFERENCES items (name),
                            FOREIGN KEY (ingredient5) REFERENCES items (name),
                            FOREIGN KEY (ingredient6) REFERENCES items (name),
                            FOREIGN KEY (ingredient7) REFERENCES items (name),
                            FOREIGN KEY (ingredient8) REFERENCES items (name)
                            )""")

        all_recipes = self.get_all_recipes()
        for recipe in all_recipes:
            name, crystal, ingredient1, ingredient2, ingredient3, \
                ingredient4, ingredient5, ingredient6, ingredient7, \
                ingredient8, synth_yield, synth_cost = recipe

            self.cur.execute("""INSERT INTO recipes_temp VALUES (:name,
                             :crystal, :ingredient1, :ingredient2,
                             :ingredient3, :ingredient4, :ingredient5,
                             :ingredient6, :ingredient7, :ingredient8,
                             :synth_yield, :synth_cost)""",
                             {
                                 "name": name,
                                 "crystal": crystal,
                                 "ingredient1": ingredient1,
                                 "ingredient2": ingredient2,
                                 "ingredient3": ingredient3,
                                 "ingredient4": ingredient4,
                                 "ingredient5": ingredient5,
                                 "ingredient6": ingredient6,
                                 "ingredient7": ingredient7,
                                 "ingredient8": ingredient8,
                                 "synth_yield": synth_yield,
                                 "synth_cost": synth_cost
                             })
            self.commit()

        self.cur.execute("DROP TABLE recipes")

        self.cur.execute("ALTER TABLE recipes_temp RENAME TO recipes")

        self.connection.execute("PRAGMA foreign_keys = 1")

    def recreate_auction_listings_table(self):
        self.connection.execute("PRAGMA foreign_keys = 0")

        self.cur.execute("""CREATE TABLE auction_listings_temp (
                            name text NOT NULL,
                            quantity integer NOT NULL,
                            price integer NOT NULL,
                            sell_freq real NOT NULL,
                            PRIMARY KEY (name, quantity),
                            FOREIGN KEY (name) REFERENCES items (name)
                            )""")

        self.cur.execute("""INSERT INTO auction_listings_temp (name, quantity,
                         price, sell_freq)
                         SELECT name, quantity, price, sell_freq
                         FROM auction_listings""")
        self.commit()

        self.cur.execute("DROP TABLE auction_listings")

        self.cur.execute("""ALTER TABLE auction_listings_temp
                         RENAME TO auction_listings""")

        self.connection.execute("PRAGMA foreign_keys = 1")

    def recreate_all_tables(self):
        self.recreate_items_table()
        self.recreate_recipes_table()
        self.recreate_auction_listings_table()
