from services import ItemService


class ItemController:
    @classmethod
    def update_auction_data(cls, item_id):
        ItemService.update_auction_data(item_id)

    @classmethod
    def update_vendor_data(cls, item_id):
        ItemService.update_vendor_data(item_id)
