from colorama import Fore, init

# Auto reset style with colorama
init(autoreset=True)


class TextUI:
    def __init__(self) -> None:
        pass

    # @staticmethod
    # def prompt_vendor_price():
    #     vendor_purchasable = input("Is it purchasable from a vendor? (y/n) ")
    #     if vendor_purchasable == "y":
    #         vendor_price = input("Enter the vendor price: ")
    #         vendor_price = int(vendor_price)
    #     else:
    #         vendor_price = None

    #     return vendor_price

    # @staticmethod
    # def prompt_recipe_name():
    #     return input("Enter the recipe name: ")

    # @staticmethod
    # def prompt_crystal():
    #     return input("Enter the crystal: ")

    # @staticmethod
    # def prompt_ingredients():
    #     ingredients = input("Enter the list of ingredients separated by " +
    #                         "commas: ")
    #     return ingredients.split(", ")

    # @staticmethod
    # def prompt_yields():
    #     nq_yield = input("Enter the NQ yield: ")
    #     hq1_yield = input("Enter the HQ1 yield: ")
    #     hq2_yield = input("Enter the HQ2 yield: ")
    #     hq3_yield = input("Enter the HQ3 yield: ")

    #     nq_yield = int(nq_yield)
    #     hq1_yield = int(hq1_yield)
    #     hq2_yield = int(hq2_yield)
    #     hq3_yield = int(hq3_yield)

    #     return nq_yield, hq1_yield, hq2_yield, hq3_yield

    # @staticmethod
    # def prompt_craft():
    #     return input("Enter the craft: ")

    # @staticmethod
    # def prompt_skill_cap():
    #     return input("Enter the skill cap: ")

    # @classmethod
    # def prompt_recipe(cls):
    #     recipe_name = cls.prompt_recipe_name()
    #     crystal = cls.prompt_crystal()
    #     ingredients = cls.prompt_ingredients()
    #     expanded_ingredients = expand_list(ingredients)
    #     nq_yield, hq1_yield, hq2_yield, hq3_yield = cls.prompt_yields()
    #     craft = cls.prompt_craft()
    #     skill_cap = cls.prompt_skill_cap()

    #     return recipe_name, crystal, expanded_ingredients, nq_yield, \
    #         hq1_yield, hq2_yield, hq3_yield, craft, skill_cap

    # @classmethod
    # def prompt_recipe_short(cls):
    #     recipe_name = cls.prompt_recipe_name()
    #     crystal = cls.prompt_crystal()
    #     ingredients = cls.prompt_ingredients()

    #     expanded_ingredients = expand_list(ingredients)

    #     return recipe_name, crystal, expanded_ingredients

    # @staticmethod
    # def prompt_price():
    #     price = input("Enter the price: ")
    #     price = int(price)
    #     return price

    # @staticmethod
    # def prompt_product():
    #     profit_threshold = input("Enter profit threshold: ")
    #     freq_treshold = input("Enter frequency threshold: ")
    #     profit_threshold = int(profit_threshold)
    #     freq_treshold = int(freq_treshold)

    #     return profit_threshold, freq_treshold

    # @staticmethod
    # def print_error_recipe_exists(recipe_name):
    #     print(Fore.RED + "Recipe \"{}\" is already in the database"
    #               .format(recipe_name))

    # @staticmethod
    # def print_error_recipe_not_exists(recipe_name):
    #     print(Fore.RED + "Recipe for \"{}\" does not exist in the database"
    #           .format(recipe_name))

    # @staticmethod
    # def print_error_listing_not_exists(listing_name):
    #     print(Fore.RED + "Listings for \"{}\" do not exist in the database"
    #           .format(listing_name))

    # @ staticmethod
    # def print_error_recipe_integrity(item_name):
    #     print(Fore.RED + "Failed to add recipe for \"{}\":".format(item_name) +
    #           " a necessary item was not found or the recipe already exists")

    # @ staticmethod
    # def print_add_recipe_success(recipe_name):
    #     print(Fore.GREEN + "Recipe for \"{}\" added successfully"
    #           .format(recipe_name))

    # @ staticmethod
    # def print_remove_listings_success(item_name):
    #     print(Fore.GREEN + "Removed auction listings for \"{}\""
    #           .format(item_name))

    # @ staticmethod
    # def print_remove_recipe_success(recipe_name):
    #     print(Fore.GREEN + "Removed recipe for \"{}\"".format(recipe_name))

    # @ staticmethod
    # def print_update_data_success():
    #     print(Fore.GREEN + "Successfully updated AH data and recipe costs")

    # @ staticmethod
    # def print_update_price_success(item_name):
    #     print(Fore.GREEN + "Updated vendor price for \"{}\"".format(item_name))

    # @ staticmethod
    # def get_table(column_names, rows):
    #     table = PrettyTable(column_names)

    #     for name in column_names:
    #         table.align[name] = "l"

    #     for row in rows:
    #         table.add_row(row)

    #     return table

    # @ classmethod
    # def print_products(cls, products):
    #     rows = []
    #     for product in products:
    #         row = [product.name, product.quantity, product.cost,
    #                product.sell_price, product.profit, product.sell_freq]
    #         rows.append(row)

    #     table = cls.get_table(["Name", "Quantity", "Cost", "Sell Price",
    #                            "Profit", "Sell Frequency"], rows)
    #     print(table)
