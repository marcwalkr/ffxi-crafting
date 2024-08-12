from config import SettingsManager
from database import Database
from repositories import VendorRepository


class VendorController:
    """
    Controller for fetching vendor costs.

    This class provides methods to interact with vendors,
    including retrieving pricing information for items.
    """

    def __init__(self, db: Database) -> None:
        """
        Initializes the VendorController.

        Args:
            db (Database): The database connection object.
        """
        self._vendor_repository: VendorRepository = VendorRepository(db)

    def get_min_cost(self, item_id: int) -> int | None:
        """
        Retrieves the min vendor cost for the item, filters out vendors based on
        beastmen-controlled regions and conquest rankings, and returns the lowest available price.

        Args:
            item_id (int): The ID of the item to fetch vendor cost for.

        Returns:
            int | None: The lowest vendor cost for the item, or None if not available.
        """
        vendor_items = self._vendor_repository.get_vendor_items(item_id)

        filtered_vendor_items = self._filter_beastmen_controlled_vendors(vendor_items)
        filtered_vendor_items = self._filter_by_conquest_rank(filtered_vendor_items)

        prices = [vendor_item.price for vendor_item in filtered_vendor_items]

        return min(prices, default=None)

    def _filter_beastmen_controlled_vendors(self, vendor_items: list) -> list:
        """
        Checks each vendor item against the list of beastmen-controlled regions
        and removes those that are in such regions. Non-regional vendors are always included.

        Args:
            vendor_items (list): List of vendor items to filter.

        Returns:
            list: Filtered list of vendor items, excluding those in beastmen-controlled regions.
        """
        beastmen_regions = SettingsManager.get_beastmen_regions()
        filtered_items = []

        for vendor_item in vendor_items:
            regional_vendor = self._vendor_repository.get_regional_vendor(vendor_item.npc_id)
            if not regional_vendor:
                # Standard vendor, always include
                filtered_items.append(vendor_item)
            else:
                vendor_region = regional_vendor.region.lower()
                if vendor_region not in beastmen_regions:
                    filtered_items.append(vendor_item)

        return filtered_items

    def _filter_by_conquest_rank(self, vendor_items: list) -> list:
        """
        Checks each vendor item against the current conquest rankings
        and includes only those that are available based on the current ranks.
        Vendors with no rank requirement (rank 0) are always included.
        The ranking system is as follows:
        - 1: 1st rank (best)
        - 2: 2nd rank
        - 3: 3rd rank
        A lower number indicates a better rank.

        Args:
            vendor_items (list): List of vendor items to filter.

        Returns:
            list: Filtered list of vendor items, including only those that are available
                  given the current conquest rankings.
        """
        sandoria_rank = SettingsManager.get_sandoria_rank()
        bastok_rank = SettingsManager.get_bastok_rank()
        windurst_rank = SettingsManager.get_windurst_rank()

        filtered_items = []

        for vendor_item in vendor_items:
            if (vendor_item.sandoria_rank == 0 or vendor_item.sandoria_rank >= sandoria_rank) and \
               (vendor_item.bastok_rank == 0 or vendor_item.bastok_rank >= bastok_rank) and \
               (vendor_item.windurst_rank == 0 or vendor_item.windurst_rank >= windurst_rank):
                filtered_items.append(vendor_item)

        return filtered_items
