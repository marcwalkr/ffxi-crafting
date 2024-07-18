from ..services import ItemService


class ItemController:
    @classmethod
    def get_item(cls, item_id):
        return ItemService.get_item(item_id)

    @classmethod
    def update_auction_data(cls, item_id):
        ItemService.update_auction_data(item_id)

    @classmethod
    def update_vendor_data(cls, item_id):
        ItemService.update_vendor_data(item_id)
