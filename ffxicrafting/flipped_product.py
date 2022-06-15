from product import Product
from controllers.vendor_controller import VendorController
from controllers.item_controller import ItemController
from controllers.auction_controller import AuctionController
from controllers.npc_controller import NpcController


class FlippedProduct(Product):
    def __init__(self, vendor_name, item_name, quantity, sell_price,
                 sell_frequency, cost) -> None:
        super().__init__(item_name, quantity, sell_price, sell_frequency, cost)
        self.vendor_name = vendor_name

    @classmethod
    def get_products(cls, profit, frequency, value):
        products = []
        vendor_items = VendorController.get_all_vendor_items()

        for vendor_item in vendor_items:
            item = ItemController.get_item(vendor_item.item_id)

            # Item cannot be sold on AH
            if item.ah == 0:
                continue

            item_name = item.sort_name.replace("_", " ").title()

            npc = NpcController.get_npc(vendor_item.npc_id)
            npc_name = npc.polutils_name

            single_cost = vendor_item.price
            stack_cost = single_cost * item.stack_size

            auction = AuctionController.get_auction(vendor_item.item_id)

            if auction.single_price is not None:
                single_product = cls(npc_name, item_name, 1,
                                     auction.single_price,
                                     auction.single_frequency, single_cost)
                products.append(single_product)

            if auction.stack_price is not None:
                stack_product = cls(npc_name, item_name,
                                    item.stack_size, auction.stack_price,
                                    auction.stack_frequency, stack_cost)
                products.append(stack_product)

        # Sort by value (function of profit and sell frequency)
        products.sort(key=lambda x: x.value, reverse=True)

        filtered_products = cls.filter_products(products, profit, frequency,
                                                value)
        return filtered_products
