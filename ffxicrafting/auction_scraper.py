import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import time
from logger import Logger


class AuctionScraper:
    def __init__(self, item_name, item_id=None) -> None:
        self.item_name = item_name

        if item_id is None:
            self.item_id = self.scrape_search()
        else:
            self.item_id = str(item_id)

        if self.item_id is not None:
            self.quantities, self.prices, self.dates = self.scrape_listing()

            self.single_price = self.get_single_price()
            self.stack_price = self.get_stack_price()

            self.single_frequency = self.get_single_frequency()
            self.stack_frequency = self.get_stack_frequency()

    def scrape_search(self):
        search_html = self.get_search_html()

        item_tags = search_html.find_all("a", {"class": "character"})

        if len(item_tags) > 1:
            index = self.prompt_correct_index(item_tags)
            correct_tag = item_tags[index]
        elif len(item_tags) == 1:
            correct_tag = item_tags[0]
        else:
            # Item not found
            return None

        item_url = correct_tag["href"]
        item_id = item_url.split("&")[-1][3:]

        return item_id

    def scrape_listing(self):
        listing_html = self.get_listing_html()

        full_item_name = listing_html.find("h2").get_text()
        Logger.print_cyan("Scraping item: {}".format(full_item_name))

        seller_buyer_quantity_tags = listing_html.find_all(
            "td", {"style": "width: 10px;"})
        price_date_tags = self.get_listing_html().find_all(
            "td", {"style": "width: 10px; text-align: right"})

        quantities = []
        for tag in seller_buyer_quantity_tags:
            tag_text = tag.get_text()
            if tag_text == "Seller":
                break
            elif tag_text != "Single" and tag_text != "Stack":
                continue
            else:
                quantities.append(tag_text)

        dates = []
        prices = []
        for tag in price_date_tags:
            tag_text = tag.get_text()
            if tag_text == "Date":
                continue
            elif "/" in tag_text:
                dates.append(tag_text)
            else:
                prices.append(tag_text)

        # Remove elements from the end of prices to match the length of dates
        # The last few prices are from bazaars
        prices = prices[:len(dates)]

        return quantities, prices, dates

    def get_url_formatted_name(self):
        # Replace spaces with +
        formatted_name = self.item_name.replace(" ", "+")
        # Remove single quotes, search fails on items with apostrophes
        formatted_name = formatted_name.replace("'", "")

        return formatted_name

    def get_search_html(self):
        url_formatted_name = self.get_url_formatted_name()

        url = "https://www.wingsxi.com/wings/index.php?page=itemsearch&name=" + \
            url_formatted_name + "&worldid=100"

        result = requests.get(url)
        html = BeautifulSoup(result.text, "html.parser")

        # Wait 3 seconds so it's not scraping to fast
        time.sleep(3)

        return html

    def get_listing_html(self):
        url = "https://www.wingsxi.com/wings/index.php?page=item&worldid=100&id=" + \
            self.item_id

        result = requests.get(url)
        html = BeautifulSoup(result.text, "html.parser")

        # Wait 3 seconds so it's not scraping to fast
        time.sleep(3)

        return html

    def get_single_price(self):
        try:
            single_index = self.quantities.index("Single")
            single_price = self.prices[single_index]
            return int(single_price)
        except ValueError:
            return None

    def get_stack_price(self):
        try:
            stack_index = self.quantities.index("Stack")
            stack_price = self.prices[stack_index]
            return int(stack_price)
        except ValueError:
            return None

    def get_num_days(self):
        """Gets the number of days from the first in history until today,
        inclusive, for calculating sell frequency
        """
        try:
            first_date_str = self.dates[-1]
            year, month, day = first_date_str.split("/")
            first_date = date(int(year), int(month), int(day))

            # Dates are in UTC on website
            today_utc = datetime.utcnow().date()
            delta = today_utc - first_date

            return delta.days + 1

        except IndexError:
            return 0

    def get_single_frequency(self):
        try:
            single_count = self.quantities.count("Single")
            freq = single_count / self.get_num_days()
            return freq
        except (ValueError, ZeroDivisionError):
            return None

    def get_stack_frequency(self):
        try:
            stack_count = self.quantities.count("Stack")
            freq = stack_count / self.get_num_days()
            return freq
        except (ValueError, ZeroDivisionError):
            return None

    def prompt_correct_index(self, item_tags):
        for i, tag in enumerate(item_tags):
            full_item_name = tag.get_text()
            Logger.print_yello("{}. {}".format(str(i), full_item_name))

        prompt_str = Logger.get_yellow(
            "Enter the correct index for the item \"{}\": ".format(self.item_name))

        correct_index = input(prompt_str)

        return int(correct_index)
