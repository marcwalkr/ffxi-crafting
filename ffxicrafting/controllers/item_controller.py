from services import ItemService


class ItemController:
    def __init__(self, db) -> None:
        self.item_service = ItemService(db)

    def update_auction_data(self, item_id):
        self.item_service.update_auction_data(item_id)

    def update_vendor_data(self, item_id):
        self.item_service.update_vendor_data(item_id)
