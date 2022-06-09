class AuctionHistory:
    def __init__(self, item_id, sellers, buyers, quantities, prices,
                 dates) -> None:
        self.item_id = item_id
        self.sellers = sellers
        self.buyers = buyers
        self.quantities = quantities
        self.prices = prices
        self.dates = dates
