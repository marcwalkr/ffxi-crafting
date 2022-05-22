from colorama import Fore, init
from helpers import expand_list
from prettytable import PrettyTable

# Auto reset style with colorama
init(autoreset=True)


class TextUI:
    def __init__(self) -> None:
        pass

    @staticmethod
    def prompt_item_name():
        return input("Enter the item name: ")

    @staticmethod
    def prompt_stack_quantity():
        stackable = input("Is it stackable? (y/n): ")
        if stackable == "y":
            stack_quantity = input("Enter the stack quantity: ")
            stack_quantity = int(stack_quantity)
        else:
            stack_quantity = None

        return stack_quantity

    @staticmethod
    def prompt_vendor_price():
        vendor_purchasable = input("Is it purchasable from a vendor? (y/n) ")
        if vendor_purchasable == "y":
            vendor_price = input("Enter the vendor price: ")
            vendor_price = int(vendor_price)
        else:
            vendor_price = None

        return vendor_price

    @classmethod
    def prompt_item(cls):
        item_name = cls.prompt_item_name()
        stack_quantity = cls.prompt_stack_quantity()
        vendor_price = cls.prompt_vendor_price()

        return item_name, stack_quantity, vendor_price

    @staticmethod
    def prompt_recipe_name():
        return input("Enter the recipe name: ")

    @staticmethod
    def prompt_synth_yield():
        synth_yield = input("Enter the synth yield: ")
        synth_yield = int(synth_yield)

        return synth_yield

    @staticmethod
    def prompt_crystal():
        return input("Enter the crystal: ")

    @staticmethod
    def prompt_ingredients():
        ingredients = input("Enter the list of ingredients separated by " +
                            "commas: ")
        return ingredients.split(", ")

    @classmethod
    def prompt_recipe(cls):
        recipe_name = cls.prompt_recipe_name()
        synth_yield = cls.prompt_synth_yield()
        crystal = cls.prompt_crystal()
        ingredients = cls.prompt_ingredients()

        expanded_ingredients = expand_list(ingredients)

        return recipe_name, synth_yield, crystal, expanded_ingredients

    @classmethod
    def prompt_recipe_short(cls):
        recipe_name = cls.prompt_recipe_name()
        crystal = cls.prompt_crystal()
        ingredients = cls.prompt_ingredients()

        expanded_ingredients = expand_list(ingredients)

        return recipe_name, crystal, expanded_ingredients

    @staticmethod
    def prompt_price():
        price = input("Enter the price: ")
        price = int(price)
        return price

    @staticmethod
    def prompt_product():
        profit_threshold = input("Enter profit threshold: ")
        freq_treshold = input("Enter frequency threshold: ")
        profit_threshold = int(profit_threshold)
        freq_treshold = int(freq_treshold)

        return profit_threshold, freq_treshold

    @staticmethod
    def prompt_command():
        command = input("1. Add an item\n" +
                        "2. Add a recipe\n" +
                        "3. Remove an item\n" +
                        "4. Remove a recipe\n" +
                        "5. Remove auction listings\n" +
                        "6. Update a vendor price\n" +
                        "7. Update AH data and recipe costs\n" +
                        "8. Print an item\n" +
                        "9. Print recipes for an item\n" +
                        "10. Print an item's auction listings\n" +
                        "11. Print products\n" +
                        "Q. Quit\n")
        return command

    @staticmethod
    def print_error_item_exists(item_name):
        print(Fore.RED + "Item \"{}\" is already in the database"
              .format(item_name))

    @staticmethod
    def print_error_item_not_exists(item_name):
        print(Fore.RED + "Item \"{}\" does not exist in the database"
              .format(item_name))

    @staticmethod
    def print_error_recipe_exists(recipe_name):
        print(Fore.RED + "Recipe \"{}\" is already in the database"
                  .format(recipe_name))

    @staticmethod
    def print_error_recipe_not_exists(recipe_name):
        print(Fore.RED + "Recipe for \"{}\" does not exist in the database"
              .format(recipe_name))

    @staticmethod
    def print_error_listing_not_exists(listing_name):
        print(Fore.RED + "Listings for \"{}\" do not exist in the database"
              .format(listing_name))

    @staticmethod
    def print_error_item_integrity(item_name):
        print(Fore.RED + "Failed to remove \"{}\":".format(item_name) +
              " a recipe or auction listing references it")

    @ staticmethod
    def print_error_recipe_integrity(item_name):
        print(Fore.RED + "Failed to add recipe for \"{}\":".format(item_name) +
              " a necessary item was not found or the recipe already exists")

    @ staticmethod
    def print_add_item_success(item_name):
        print(Fore.GREEN + "Item \"{}\" added successfully".format(item_name))

    @ staticmethod
    def print_add_recipe_success(recipe_name):
        print(Fore.GREEN + "Recipe for \"{}\" added successfully"
              .format(recipe_name))

    @ staticmethod
    def print_remove_listings_success(item_name):
        print(Fore.GREEN + "Removed auction listings for \"{}\""
              .format(item_name))

    @ staticmethod
    def print_remove_item_success(item_name):
        print(Fore.GREEN + "Removed item \"{}\"".format(item_name))

    @ staticmethod
    def print_remove_recipe_success(recipe_name):
        print(Fore.GREEN + "Removed recipe for \"{}\"".format(recipe_name))

    @ staticmethod
    def print_update_data_success():
        print(Fore.GREEN + "Successfully updated AH data and recipe costs")

    @ staticmethod
    def print_update_price_success(item_name):
        print(Fore.GREEN + "Updated vendor price for \"{}\"".format(item_name))

    @ staticmethod
    def print_error(error_text):
        print(Fore.RED + error_text)

    @ staticmethod
    def get_table(column_names, rows):
        table = PrettyTable(column_names)

        for name in column_names:
            table.align[name] = "l"

        for row in rows:
            table.add_row(row)

        return table

    @ classmethod
    def print_item(cls, item):
        rows = [[item.name, item.stack_quantity, item.vendor_price]]
        table = cls.get_table(["Name", "Stack Quantity", "Vendor Price"], rows)
        print(table)

    @ classmethod
    def print_recipes(cls, recipes):
        rows = []
        for recipe in recipes:
            row = [recipe.name, recipe.synth_yield, recipe.synth_cost,
                   recipe.crystal]
            row += recipe.ingredients
            rows.append(row)

        table = cls.get_table(["Name", "Synth Yield", "Synth Cost", "Crystal",
                               "Ingredient 1", "Ingredient 2", "Ingredient 3",
                              "Ingredient 4", "Ingredient 5", "Ingredient 6",
                               "Ingredient 7", "Ingredient 8"], rows)
        print(table)

    @ classmethod
    def print_auction_listings(cls, listings):
        rows = []
        for listing in listings:
            row = [listing.name, listing.quantity, listing.price,
                   listing.sell_freq]
            rows.append(row)

        table = cls.get_table(["Item Name", "Quantity", "Price",
                               "Sell Frequency"], rows)
        print(table)

    @ classmethod
    def print_products(cls, products):
        rows = []
        for product in products:
            row = [product.name, product.quantity, product.cost,
                   product.sell_price, product.profit, product.sell_freq]
            rows.append(row)

        table = cls.get_table(["Name", "Quantity", "Cost", "Sell Price",
                               "Profit", "Sell Frequency"], rows)
        print(table)
