from repositories import AuctionRepository


class AuctionController:
    def __init__(self, db) -> None:
        self.auction_repository = AuctionRepository(db)

    def get_auction_items_with_updates(self, item_id):
        auction_items = self.auction_repository.get_auction_items(item_id)
        for item in auction_items:
            if item.new_data:
                new_sales_history = self.auction_repository.get_latest_sales_history(item.item_id, item.is_stack)
                updated_item = self.process_new_data(item, new_sales_history)
                self.auction_repository.update_auction_item(updated_item)
        return auction_items

    def process_new_data(self, item, new_sales_history):
        if not new_sales_history:
            return item
        prices = [sale.price for sale in new_sales_history]
        avg_price = sum(prices) / len(prices)
        item.avg_price = avg_price
        item.sell_freq = item.num_sales / 15
        return item
