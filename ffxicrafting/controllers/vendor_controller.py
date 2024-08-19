from database import Database
from controllers import NpcController
from entities import VendorItem, RegionalVendorItem
from repositories import VendorRepository


class VendorController:
    """
    Controller for fetching vendor costs.

    This class provides methods to create and retrieve vendor objects using data from VendorRepository.
    """

    def __init__(self, db: Database) -> None:
        """
        Initializes the VendorController.

        Args:
            db (Database): The database connection object.
        """
        self._vendor_repository: VendorRepository = VendorRepository(db)
        self._npc_controller: NpcController = NpcController(db)

    def get_vendor_items(self, item_id: int) -> list[any]:
        """
        Retrieves the vendor items for the given item ID.

        Args:
            item_id (int): The ID of the item to fetch vendor items for.

        Returns:
            list[any]: The vendor items for the given item ID. Can contain VendorItem or RegionalVendorItem.
        """
        vendor_items = self._vendor_repository.get_vendor_items(item_id)
        for item in vendor_items:
            npc = self._npc_controller.get_npc(item.npc_id)
            regional_vendor = self._vendor_repository.get_regional_vendor(item.npc_id)
            if regional_vendor:
                regional_vendor_item = RegionalVendorItem(item.item_id, item.npc_id, item.min_price,
                                                          item.sandoria_rank, item.bastok_rank, item.windurst_rank,
                                                          item.sandoria_citizen, item.bastok_citizen,
                                                          item.windurst_citizen, npc, regional_vendor.region)
                vendor_items.append(regional_vendor_item)
            else:
                vendor_item = VendorItem(item.item_id, item.npc_id, item.min_price, item.sandoria_rank,
                                         item.bastok_rank, item.windurst_rank, item.sandoria_citizen,
                                         item.bastok_citizen, item.windurst_citizen, npc)
                vendor_items.append(vendor_item)
        return vendor_items
