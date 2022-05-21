from item import Item
from recipe import Recipe
from auction_listing import AuctionListing
from product import Product
from prettytable import PrettyTable
import re
from colorama import Fore, init

# Auto reset style with colorama
init(autoreset=True)


def add_item():
    item_name = input("Enter the item name: ")

    stackable = input("Is it stackable? (y/n): ")
    if stackable == "y":
        stack_quantity = input("Enter the stack quantity: ")
        stack_quantity = int(stack_quantity)
    else:
        stack_quantity = None

    vendor_purchasable = input("Is it purchasable from a vendor? (y/n) ")
    if vendor_purchasable == "y":
        vendor_price = input("Enter the vendor price: ")
        vendor_price = int(vendor_price)
    else:
        vendor_price = None

    item = Item(item_name, stack_quantity, vendor_price)

    if Item.is_in_database(item_name):
        print(Fore.RED + "Item \"{}\" is already in the database"
              .format(item_name))
        return

    try:
        listings = AuctionListing.scrape_listings(item_name, stack_quantity)
        item.add_to_database()

        for listing in listings:
            listing.add_to_database()

        print(Fore.GREEN + "Item \"{}\" added successfully".format(item_name))
    except ValueError as e:
        print(Fore.RED + str(e))


def remove_item():
    item_name = input("Enter the item name: ")
    if not Item.is_in_database(item_name):
        print(Fore.RED + "Item \"{}\" does not exist in the database"
              .format(item_name))
    else:
        Item.remove_item(item_name)
        print(Fore.GREEN + "Removed item \"{}\"".format(item_name))


def add_recipe():
    recipe_name = input("Enter the recipe name: ")
    synth_yield = input("Enter the synth yield: ")
    synth_yield = int(synth_yield)
    crystal = input("Enter the crystal: ")
    ingredients = input("Enter the list of ingredients separated by commas: ")
    ingredients = ingredients.split(", ")

    expanded_ingredients = expand_ingredients(ingredients)

    try:
        recipe = Recipe(recipe_name, crystal,
                        expanded_ingredients, synth_yield)

        if Recipe.is_in_database(recipe_name, crystal, expanded_ingredients):
            print(Fore.RED + "Recipe \"{}\" is already in the database"
                  .format(recipe_name))
            return

        recipe.add_to_database()

        print(Fore.GREEN + "Recipe for \"{}\" added successfully".format(recipe_name))
    except ValueError as e:
        print(Fore.RED + str(e))


def expand_ingredients(condensed_ingredients):
    """Removes numbers and expands list e.g. Item x3 -> Item Item Item"""
    expanded_ingredients = []
    for ingredient in condensed_ingredients:
        num_found = re.search(r"\d+", ingredient)
        if num_found:
            num = int(num_found.group(0))
            name_without_num = ingredient[:ingredient.rfind(" ")]
            expanded_ingredients += [name_without_num] * num
        else:
            expanded_ingredients.append(ingredient)

    return expanded_ingredients


def remove_recipe():
    recipe_name = input("Enter the recipe name: ")
    crystal = input("Enter the recipe crystal: ")
    ingredients = input("Enter the list of ingredients separated by commas: ")
    ingredients = ingredients.split(", ")
    expanded_ingredients = expand_ingredients(ingredients)

    if not Recipe.is_in_database(recipe_name, crystal, expand_ingredients):
        print(Fore.RED + "Recipe for \"{}\" does not exist in the database"
              .format(recipe_name))
    else:
        Recipe.remove_recipe(recipe_name, crystal, expanded_ingredients)
        print(Fore.GREEN + "Removed recipe for \"{}\"".format(recipe_name))


def remove_auction_listings():
    listing_name = input("Enter the item name: ")
    if not AuctionListing.is_in_database(listing_name):
        print(Fore.RED + "Listings for \"{}\" do not exist in the database"
              .format(listing_name))
    else:
        AuctionListing.remove_listings(listing_name)
        print(Fore.GREEN + "Removed auction listings for \"{}\"".format(listing_name))


def update_ah_data_and_recipe_costs():
    AuctionListing.update_ah_data()
    Recipe.update_recipe_costs()
    print(Fore.GREEN + "Successfully updated AH data and recipe costs")


def update_vendor_price():
    item_name = input("Enter the item name: ")
    if not Item.is_in_database(item_name):
        print(Fore.RED + "Item \"{}\" does not exist in the database"
              .format(item_name))
    else:
        price = input("Enter the new price: ")
        price = int(price)
        Item.update_vendor_price(item_name, price)
        print(Fore.GREEN + "Updated vendor price for \"{}\"".format(item_name))


def get_table(column_names, rows):
    table = PrettyTable(column_names)

    for name in column_names:
        table.align[name] = "l"

    for row in rows:
        table.add_row(row)

    return table


def print_item():
    item_name = input("Enter the item name: ")
    item = Item.get_item(item_name)

    if item is None:
        print(Fore.RED + "Item \"{}\" does not exist in the database"
              .format(item_name))
    else:
        rows = [[item.name, item.stack_quantity, item.vendor_price]]
        table = get_table(["Name", "Stack Quantity", "Vendor Price"], rows)
        print(table)


def print_recipes():
    recipe_name = input("Enter the item name: ")
    recipes = Recipe.get_recipes(recipe_name)

    if len(recipes) == 0:
        print(Fore.RED + "Recipe for \"{}\" does not exist in the database"
              .format(recipe_name))
    else:
        rows = []
        for recipe in recipes:
            row = [recipe.name, recipe.synth_yield, recipe.synth_cost,
                   recipe.crystal]
            row += recipe.ingredients
            rows.append(row)

        table = get_table(["Name", "Synth Yield", "Synth Cost", "Crystal",
                           "Ingredient 1", "Ingredient 2", "Ingredient 3",
                           "Ingredient 4", "Ingredient 5", "Ingredient 6",
                           "Ingredient 7", "Ingredient 8"], rows)
        print(table)


def print_auction_listings():
    item_name = input("Enter the item name: ")
    listings = AuctionListing.get_listings(item_name)

    if len(listings) == 0:
        print(Fore.RED + "Listings for \"{}\" do not exist in the database".
              format(item_name))
    else:
        rows = []
        for listing in listings:
            row = [listing.name, listing.quantity, listing.price,
                   listing.sell_freq]
            rows.append(row)

        table = get_table(["Item Name", "Quantity", "Price", "Sell Frequency"],
                          rows)

        print(table)


def print_product_table():
    profit_threshold = input("Enter profit threshold: ")
    freq_treshold = input("Enter frequency threshold: ")
    profit_threshold = int(profit_threshold)
    freq_treshold = int(freq_treshold)

    products = Product.get_products(profit_threshold, freq_treshold)

    rows = []
    for product in products:
        row = [product.name, product.quantity, product.cost,
               product.sell_price, product.profit, product.sell_freq]
        rows.append(row)

    table = get_table(["Name", "Quantity", "Cost", "Sell Price", "Profit",
                       "Sell Frequency"], rows)

    print(table)


if __name__ == "__main__":
    while True:
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

        if command == "1":
            add_item()
        elif command == "2":
            add_recipe()
        elif command == "3":
            remove_item()
        elif command == "4":
            remove_recipe()
        elif command == "5":
            remove_auction_listings()
        elif command == "6":
            update_vendor_price()
        elif command == "7":
            update_ah_data_and_recipe_costs()
        elif command == "8":
            print_item()
        elif command == "9":
            print_recipes()
        elif command == "10":
            print_auction_listings()
        elif command == "11":
            print_product_table()
        elif command == "q" or command == "Q":
            break
