from sqlite3 import IntegrityError
from item import Item
from recipe import Recipe
from auction_listing import AuctionListing
from auction_scraper import AuctionScraper
from product import Product
from text_ui import TextUI


def add_item():
    item_name, stack_quantity = TextUI.prompt_item()

    try:
        # Scrape and verify the item exists on AH before adding the item
        scraper = AuctionScraper(item_name)

        # Create the item and add to db
        item = Item(item_name, scraper.full_item_name, stack_quantity)
        item.to_database()

        # Create auction listings for single and stack, add to db
        if scraper.single_price is not None:
            single_listing = AuctionListing(item_name, False,
                                            scraper.single_price, scraper.single_freq)
            single_listing.to_database()

        if scraper.stack_price is not None:
            stack_listing = AuctionListing(item_name, True, scraper.stack_price,
                                           scraper.stack_freq)
            stack_listing.to_database()

        TextUI.print_add_item_success(item_name)

    except IntegrityError:
        TextUI.print_error_item_in_db(item_name)
    except ValueError:
        TextUI.print_error_item_not_on_ah(item_name)


def remove_item():
    item_name = TextUI.prompt_item_name()

    if not Item.is_in_database(item_name):
        TextUI.print_error_item_not_in_db(item_name)
        return

    try:
        Item.remove_item(item_name)
        TextUI.print_remove_item_success(item_name)
    except IntegrityError:
        TextUI.print_error_item_integrity(item_name)

    # def add_recipe():
    #     recipe_name, crystal, ingredients, nq_yield, hq1_yield, hq2_yield, \
    #         hq3_yield, craft, skill_cap = TextUI.prompt_recipe()

    #     try:
    #         recipe = Recipe(recipe_name, crystal, ingredients, nq_yield,
    #                         hq1_yield, hq2_yield, hq3_yield, craft, skill_cap)

    #         if Recipe.is_in_database(recipe_name, crystal, ingredients):
    #             TextUI.print_error_recipe_exists(recipe_name)
    #             return

    #         recipe.add_to_database()

    #         TextUI.print_add_recipe_success(recipe_name)
    #     except IntegrityError:
    #         TextUI.print_error_recipe_integrity(recipe_name)
    #     except ValueError as e:
    #         TextUI.print_error(str(e))

    # def remove_recipe():
    #     recipe_name, crystal, ingredients = TextUI.prompt_recipe_short()

    #     if not Recipe.is_in_database(recipe_name, crystal, ingredients):
    #         TextUI.print_error_recipe_not_exists(recipe_name)
    #     else:
    #         Recipe.remove_recipe(recipe_name, crystal, ingredients)
    #         TextUI.print_remove_recipe_success(recipe_name)

    # def remove_auction_listings():
    #     item_name = TextUI.prompt_item_name()
    #     if not AuctionListing.is_in_database(item_name):
    #         TextUI.print_error_listing_not_exists(item_name)
    #     else:
    #         AuctionListing.remove_listings(item_name)
    #         TextUI.print_remove_listings_success(item_name)

    # def update_ah_data_and_recipe_costs():
    #     AuctionListing.update_ah_data()
    #     Recipe.update_recipe_costs()
    #     TextUI.print_update_data_success()

    # def update_vendor_price():
    #     item_name = TextUI.prompt_item_name()
    #     if not Item.is_in_database(item_name):
    #         TextUI.print_error_item_not_exists(item_name)
    #     else:
    #         price = TextUI.prompt_price()
    #         Item.update_vendor_price(item_name, price)
    #         TextUI.print_update_price_success(item_name)

    # def print_products():
    #     profit_threshold, freq_treshold = TextUI.prompt_product()
    #     products = Product.get_products(profit_threshold, freq_treshold)
    #     TextUI.print_products(products)


if __name__ == "__main__":
    while True:
        command = TextUI.prompt_command()

        if command == "1":
            add_item()
        elif command == "2":
            remove_item()
        elif command == "q" or command == "Q":
            break
