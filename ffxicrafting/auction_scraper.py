import requests
import time
from bs4 import BeautifulSoup
from datetime import date, datetime
from helpers import chunker
from logger import Logger


class AuctionScraper:
    def __init__(self, item_id, logging=True) -> None:
        self.item_id = str(item_id)
        self.logging = logging

        self.sellers, self.buyers, self.quantities, self.prices, self.dates = \
            self.scrape_listing()

        self.single_sales = self.get_single_sales()
        self.single_price_sum = self.get_single_price_sum()

        self.stack_sales = self.get_stack_sales()
        self.stack_price_sum = self.get_stack_price_sum()

        self.days = self.get_num_days()

    def scrape_listing(self):
        listing_html = self.get_listing_html()

        full_item_name = listing_html.find("h2").get_text()

        if self.logging:
            Logger.print_cyan("Scraping item: {}".format(full_item_name))

        seller_buyer_quantity_tags = listing_html.find_all(
            "td", {"style": "width: 10px;"})
        price_date_tags = self.get_listing_html().find_all(
            "td", {"style": "width: 10px; text-align: right"})

        sellers = []
        buyers = []
        quantities = []
        for group in chunker(seller_buyer_quantity_tags[2:], 3):
            try:
                seller_tag, buyer_tag, quantity_tag = group
                seller = seller_tag.get_text()
                buyer = buyer_tag.get_text()
                quantity = quantity_tag.get_text()

                # Start of bazaar html
                if seller == "Seller" or buyer == "Seller" or quantity == "Seller":
                    break

                sellers.append(seller)
                buyers.append(buyer)
                quantities.append(quantity)
            except ValueError:
                break

        prices = []
        dates = []
        for group in chunker(price_date_tags[1:], 2):
            try:
                price_tag, date_tag = group
                price = price_tag.get_text()
                date = date_tag.get_text()

                # Start of bazaar html
                if "/" not in date:
                    break

                prices.append(price)
                dates.append(date)
            except ValueError:
                break

        return sellers, buyers, quantities, prices, dates

    def get_listing_html(self):
        url = ("https://www.wingsxi.com/wings/index.php?page=item&worldid=100"
               "&id={}").format(self.item_id)

        result = requests.get(url)
        html = BeautifulSoup(result.text, "html.parser")

        # Wait 3 seconds so it's not scraping to fast
        time.sleep(3)

        return html

    def get_single_sales(self):
        return self.quantities.count("Single")

    def get_single_price_sum(self):
        sum = 0
        for i in range(len(self.quantities)):
            if self.quantities[i] == "Single":
                sum += int(self.prices[i])

        return sum

    def get_stack_sales(self):
        return self.quantities.count("Stack")

    def get_stack_price_sum(self):
        sum = 0
        for i in range(len(self.quantities)):
            if self.quantities[i] == "Stack":
                sum += int(self.prices[i])

        return sum

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
