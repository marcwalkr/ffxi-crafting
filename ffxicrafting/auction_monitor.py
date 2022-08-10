from logger import Logger
from playsound import playsound
from pathlib import Path
from auction_scraper import AuctionScraper
from controllers.item_controller import ItemController


class AuctionMonitor:
    def __init__(self, monitored_ids) -> None:
        self.monitored_ids = monitored_ids
        self.auction_histories = {}

    def monitor_auctions(self):
        self.inititialize_histories()
        Logger.print_yello("Monitoring auctions. Stop monitoring with "
                           "Ctrl+C")
        while True:
            try:
                for id in self.monitored_ids:
                    scraper = AuctionScraper(id, False)

                    if len(scraper.quantities) == 0:
                        continue

                    if self.history_changed(id, scraper.sellers, scraper.buyers):
                        item = ItemController.get_item(id)
                        item_name = item.sort_name.replace("_", " ").title()

                        quantity = scraper.quantities[0]
                        latest_seller = scraper.sellers[0]

                        self.print_sold_alert(
                            item_name, quantity, latest_seller)

                        self.auction_histories[id] = scraper

            except KeyboardInterrupt:
                break

    def inititialize_histories(self):
        Logger.print_yello("Initializing auction histories for monitoring...")

        for id in self.monitored_ids:
            scraper = AuctionScraper(id, False)
            self.auction_histories[id] = scraper

    def history_changed(self, item_id, new_sellers, new_buyers):
        history = self.auction_histories[item_id]
        sellers_changed = history.sellers != new_sellers
        buyers_changed = history.buyers != new_buyers

        return sellers_changed or buyers_changed

    @staticmethod
    def print_sold_alert(item_name, quantity, seller_name):
        Logger.print_red("Item \"{}\" ({}) was recently sold by {}"
                         .format(item_name, quantity, seller_name))
        audio = Path().cwd().__str__() + "\sounds\Alarm04.wav"
        playsound(audio)
