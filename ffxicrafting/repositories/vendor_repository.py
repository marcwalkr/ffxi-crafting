from database import Database
from models import VendorItem, RegionalVendor, VendorLocation


class VendorRepository:
    """
    Repository class for handling vendor-related data operations.

    This class provides methods to interact with the database for retrieving
    vendor item information, regional vendor data, and vendor locations.
    """

    _vendor_item_cache: dict[int, list[VendorItem]] = {}
    _regional_vendor_cache: dict[int, RegionalVendor] = {}
    _vendor_location_cache: dict[int, VendorLocation] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize a VendorRepository instance.
        All vendor data is loaded into the cache on initialization.

        Args:
            db (Database): The database connection object used for querying vendor data.
        """
        self._db = db
        if not VendorRepository._vendor_item_cache:
            self._load_vendor_items()
        if not VendorRepository._regional_vendor_cache:
            self._load_regional_vendors()
        if not VendorRepository._vendor_location_cache:
            self._load_vendor_locations()

    def _load_vendor_items(self) -> None:
        """
        Load all vendor items into the cache.
        """
        vendor_item_tuples = self._db.get_all_vendor_items()
        vendor_items = [VendorItem(*tuple) for tuple in vendor_item_tuples]

        # Group vendor items by item_id
        grouped_items = {}
        for item in vendor_items:
            if item.item_id not in grouped_items:
                grouped_items[item.item_id] = []
            grouped_items[item.item_id].append(item)

        # Update the cache with grouped items
        VendorRepository._vendor_item_cache = grouped_items

    def _load_regional_vendors(self) -> None:
        """
        Load all regional vendors into the cache.
        """
        regional_vendor_tuples = self._db.get_all_regional_vendors()
        regional_vendors = [RegionalVendor(*tuple) for tuple in regional_vendor_tuples]
        VendorRepository._regional_vendor_cache = {v.npc_id: v for v in regional_vendors}

    def _load_vendor_locations(self) -> None:
        """
        Load all vendor locations into the cache.
        """
        vendor_location_tuples = self._db.get_all_vendor_locations()
        vendor_locations = [VendorLocation(*tuple) for tuple in vendor_location_tuples]
        VendorRepository._vendor_location_cache = {v.npc_id: v for v in vendor_locations}

    def get_vendor_items(self, item_id: int) -> list[VendorItem]:
        """
        Retrieve vendor items for a given item ID from the cache.

        Args:
            item_id (int): The ID of the item to retrieve vendor information for.

        Returns:
            list[VendorItem]: A list of VendorItem objects for the given item ID.
                              Returns an empty list if no vendor items are found.
        """
        if item_id in self._vendor_item_cache:
            return self._vendor_item_cache[item_id]
        else:
            return []

    def get_regional_vendor(self, npc_id: int) -> RegionalVendor | None:
        """
        Retrieve regional vendor information for a given NPC ID from the cache.

        Args:
            npc_id (int): The ID of the NPC to retrieve regional vendor information for.

        Returns:
            RegionalVendor | None: A RegionalVendor object for the given NPC ID,
                                   or None if no regional vendor information is found.
        """
        if npc_id in self._regional_vendor_cache:
            return self._regional_vendor_cache[npc_id]
        else:
            return None

    def get_vendor_location(self, npc_id: int) -> VendorLocation | None:
        """
        Retrieve vendor location information for a given NPC ID from the cache.

        Args:
            npc_id (int): The ID of the NPC to retrieve location information for.

        Returns:
            VendorLocation | None: A VendorLocation object for the given NPC ID,
                                   or None if no vendor location information is found.
        """
        if npc_id in self._vendor_location_cache:
            return self._vendor_location_cache[npc_id]
        else:
            return None
