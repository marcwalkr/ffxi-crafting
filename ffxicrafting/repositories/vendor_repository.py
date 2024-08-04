from database import Database
from models import VendorItem, RegionalVendor, VendorLocation


class VendorRepository:
    """
    Repository class for handling vendor-related data operations.

    This class provides methods to interact with the database for retrieving
    vendor item information, regional vendor data, and vendor locations.
    It implements caching to improve performance for frequently accessed data.
    """

    _vendor_item_cache: dict[int, list[VendorItem]] = {}
    _regional_vendor_cache: dict[int, RegionalVendor] = {}
    _vendor_location_cache: dict[int, VendorLocation] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize a VendorRepository instance.

        Args:
            db (Database): The database connection object used for querying vendor data.
        """
        self._db = db

    def get_vendor_items(self, item_id: int) -> list[VendorItem]:
        """
        Retrieve vendor items for a given item ID.

        This method first checks the cache for the requested item. If not found,
        it queries the database and caches the result for future use.

        Args:
            item_id (int): The ID of the item to retrieve vendor information for.

        Returns:
            list[VendorItem]: A list of VendorItem objects for the given item ID.
                              Returns an empty list if no vendor items are found.
        """
        if item_id in self._vendor_item_cache:
            return self._vendor_item_cache[item_id]
        else:
            vendor_item_tuples = self._db.get_vendor_items(item_id)
            if vendor_item_tuples:
                self._vendor_item_cache[item_id] = [VendorItem(*v) for v in vendor_item_tuples]
                return self._vendor_item_cache[item_id]

            self._vendor_item_cache[item_id] = []
            return []

    def get_regional_vendor(self, npc_id: int) -> RegionalVendor | None:
        """
        Retrieve regional vendor information for a given NPC ID.

        This method first checks the cache for the requested regional vendor. If not found,
        it queries the database and caches the result for future use.

        Args:
            npc_id (int): The ID of the NPC to retrieve regional vendor information for.

        Returns:
            RegionalVendor | None: A RegionalVendor object for the given NPC ID,
                                   or None if no regional vendor information is found.
        """
        if npc_id in self._regional_vendor_cache:
            return self._regional_vendor_cache[npc_id]
        else:
            regional_vendor_tuple = self._db.get_regional_vendor(npc_id)
            if regional_vendor_tuple:
                self._regional_vendor_cache[npc_id] = RegionalVendor(*regional_vendor_tuple)
                return self._regional_vendor_cache[npc_id]
            return None

    def get_vendor_location(self, npc_id: int) -> VendorLocation | None:
        """
        Retrieve vendor location information for a given NPC ID.

        This method first checks the cache for the requested vendor location. If not found,
        it queries the database and caches the result for future use.

        Args:
            npc_id (int): The ID of the NPC to retrieve location information for.

        Returns:
            VendorLocation | None: A VendorLocation object for the given NPC ID,
                                   or None if no vendor location information is found.
        """
        if npc_id in self._vendor_location_cache:
            return self._vendor_location_cache[npc_id]
        else:
            vendor_location_tuple = self._db.get_vendor_location(npc_id)
            if vendor_location_tuple:
                self._vendor_location_cache[npc_id] = VendorLocation(*vendor_location_tuple)
                return self._vendor_location_cache[npc_id]
            return None
