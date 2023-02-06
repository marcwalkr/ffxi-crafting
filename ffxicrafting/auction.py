from auction_item import AuctionItem


class Auction:
    def __init__(self, auction_items) -> None:
        self.auction_items = auction_items

    def get_auction_item(self, item_name):
        for item in self.auction_items:
            if item.item_name == item_name:
                return item

        return AuctionItem(item_name, 0, 0)
