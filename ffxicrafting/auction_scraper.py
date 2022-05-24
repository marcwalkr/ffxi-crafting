import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import time
from text_ui import TextUI


class AuctionScraper:
    def __init__(self, item_name) -> None:
        self.item_name = item_name

        self.item_id, self.full_item_name = self.scrape_search()
        self.quantities, self.prices, self.dates = self.scrape_listing()
        self.is_empty_history = len(self.quantities) == 0

    def scrape_search(self):
        search_html = self.get_search_html()
        item_tags = search_html.find_all("a", {"class": "character"})

        if len(item_tags) > 1:
            index = TextUI.prompt_correct_index(self.item_name, item_tags)
            correct_tag = item_tags[index]
        elif len(item_tags) == 1:
            correct_tag = item_tags[0]
        else:
            raise ValueError("Item \"{}\" was not found on the AH"
                             .format(self.item_name))

        full_item_name = correct_tag.get_text()
        TextUI.print_scraping_item(full_item_name)

        item_url = correct_tag["href"]
        item_id = item_url.split("&")[-1][3:]

        return item_id, full_item_name

    def scrape_listing(self):
        seller_buyer_quantity_tags = self.get_listing_html().find_all(
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
        url = "https://www.wingsxi.com/wings/index.php?page=itemsearch&name=" + \
            self.get_url_formatted_name() + "&worldid=100"
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

    @property
    def single_price(self):
        if self.is_empty_history:
            return None

        try:
            single_index = self.quantities.index("Single")
            single_price = self.prices[single_index]
            return int(single_price)
        except ValueError:
            return None

    @property
    def stack_price(self):
        if self.is_empty_history:
            return None

        try:
            stack_index = self.quantities.index("Stack")
            stack_price = self.prices[stack_index]
            return int(stack_price)
        except ValueError:
            return None

    @property
    def num_days(self):
        """Gets the number of days from the first in history until today,
        inclusive, for calculating sell frequency
        """
        if self.is_empty_history:
            return 0

        first_date_str = self.dates[-1]
        year, month, day = first_date_str.split("/")
        first_date = date(int(year), int(month), int(day))
        # Dates are in UTC on website
        today_utc = datetime.utcnow().date()
        delta = today_utc - first_date

        return delta.days + 1

    @property
    def single_freq(self):
        if self.is_empty_history:
            return None

        try:
            single_count = self.quantities.count("Single")
            freq = single_count / self.num_days
            return freq
        except ValueError:
            return None

    @property
    def stack_freq(self):
        if self.is_empty_history:
            return None

        try:
            stack_count = self.quantities.count("Stack")
            freq = stack_count / self.num_days
            return freq
        except ValueError:
            return None
