import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
import time


class AuctionScraper:
    def __init__(self, item_name) -> None:
        self.item_name = item_name

        self.item_id = None
        self.quantities = None
        self.prices = None
        self.dates = None
        self.empty_price_history = None
        self.num_days = None

    def scrape(self):
        self.item_id = self.get_item_id()
        if self.item_id is None:
            raise ValueError("Error: could not find item on AH")

        self.quantities, self.prices, self.dates = self.get_ah_data()
        self.empty_price_history = len(self.quantities) == 0
        self.num_days = self.get_num_days()

    def get_item_id(self):
        search_html = self.get_search_html()
        item_tags = search_html.find_all("a", {"class": "character"})

        if len(item_tags) > 1:
            for i, tag in enumerate(item_tags):
                print(str(i) + ". " + tag.get_text())
            idx = input("Enter the correct index for the item \"" +
                        self.item_name + "\": ")
            idx = int(idx)
            item_tag = item_tags[idx]
        elif len(item_tags) == 1:
            item_tag = item_tags[0]
        else:
            return None

        print("Scraping item: " + item_tag.get_text())
        item_url = item_tag["href"]
        item_id = item_url.split("&")[-1][3:]

        return item_id

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

    def get_ah_data(self):
        listing_html = self.get_listing_html()

        seller_buyer_quantity_tags = listing_html.find_all(
            "td", {"style": "width: 10px;"})
        price_date_tags = listing_html.find_all(
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

        return [quantities, prices, dates]

    def get_single_price(self):
        if self.empty_price_history:
            return None

        try:
            single_index = self.quantities.index("Single")
            single_price = self.prices[single_index]
            return int(single_price)
        except ValueError:
            return None

    def get_stack_price(self):
        if self.empty_price_history:
            return None

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
        if self.empty_price_history:
            return 0

        first_date_str = self.dates[-1]
        year, month, day = first_date_str.split("/")
        first_date = date(int(year), int(month), int(day))
        # Dates are in UTC on website
        today_utc = datetime.utcnow().date()
        delta = today_utc - first_date

        return delta.days + 1

    def get_single_freq(self):
        if self.empty_price_history:
            return None

        try:
            single_count = self.quantities.count("Single")
            freq = single_count / self.num_days
            return freq
        except ValueError:
            return None

    def get_stack_freq(self):
        if self.empty_price_history:
            return None

        try:
            stack_count = self.quantities.count("Stack")
            freq = stack_count / self.num_days
            return freq
        except ValueError:
            return None
