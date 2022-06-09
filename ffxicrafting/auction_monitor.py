import time
from logger import Logger
from auction_scraper import AuctionScraper
from models.auction_history import AuctionHistory
from controllers.item_controller import ItemController


class AuctionMonitor:
    def __init__(self, monitored_ids, frequency) -> None:
        self.monitored_ids = monitored_ids
        self.frequency = frequency
        self.auction_histories = {}

    def monitor_auctions(self):
        self.inititialize_histories()
        Logger.print_yello("Monitoring auctions. Stop monitoring by typing "
                           "Ctrl+C")
        while True:
            try:
                for id in self.monitored_ids:
                    scraper = AuctionScraper(id, False)

                    if self.history_changed(id, scraper.sellers, scraper.buyers):
                        item = ItemController.get_item(id)
                        item_name = item.sort_name.replace("_", " ").title()

                        quantity = scraper.quantities[0]
                        latest_seller = scraper.sellers[0]

                        self.print_sold_alert(
                            item_name, quantity, latest_seller)

                        new_history = AuctionHistory(id, scraper.sellers,
                                                     scraper.buyers,
                                                     scraper.quantities,
                                                     scraper.prices,
                                                     scraper.dates)
                        self.auction_histories[id] = new_history

                time.sleep(self.frequency * 60)

            except KeyboardInterrupt:
                break

    def inititialize_histories(self):
        Logger.print_yello("Initializing auction histories for monitoring...")

        for id in self.monitored_ids:
            scraper = AuctionScraper(id, False)
            history = AuctionHistory(id, scraper.sellers, scraper.buyers,
                                     scraper.quantities, scraper.prices,
                                     scraper.dates)
            self.auction_histories[id] = history

    def history_changed(self, item_id, new_sellers, new_buyers):
        history = self.auction_histories[item_id]
        sellers_changed = history.sellers != new_sellers
        buyers_changed = history.buyers != new_buyers

        return sellers_changed or buyers_changed

    @staticmethod
    def print_sold_alert(item_name, quantity, seller_name):
        Logger.print_red("Item \"{}\" ({}) was recently sold by {}"
                         .format(item_name, quantity, seller_name))
