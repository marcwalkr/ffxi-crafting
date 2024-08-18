from database import Database
from controllers import ZoneController
from repositories import NpcRepository, VendorRepository
from entities import Npc


class NpcController:
    """
    Controller class for managing NPC-related operations.
    """

    _cache: dict[int, Npc] = {}

    def __init__(self, db: Database) -> None:
        """
        Initializes the NPC controller.

        Args:
            db (Database): The database connection object.
        """
        self._npc_repository: NpcRepository = NpcRepository(db)
        self._vendor_repository: VendorRepository = VendorRepository(db)
        self._zone_controller: ZoneController = ZoneController(db)
        if not NpcController._cache:
            self._create_npc_objects()

    def _create_npc_objects(self) -> None:
        """
        Create NPC objects from the NPC repository and cache them.
        """
        npc_models = self._npc_repository.get_all_npcs()
        for npc_model in npc_models:
            vendor_location = self._vendor_repository.get_vendor_location(npc_model.npc_id)
            zone = self._zone_controller.get_zone(vendor_location.zone_id)
            npc = Npc(npc_model.npc_id, npc_model.polutils_name, zone, vendor_location.coordinates)
            NpcController._cache[npc_model.npc_id] = npc
        self._npc_repository.delete_cache()

    def get_npc(self, npc_id: int) -> Npc:
        """
        Get an NPC object from the cache.

        Args:
            npc_id (int): The ID of the NPC to get.

        Returns:
            Npc: The NPC object.
        """
        return NpcController._cache[npc_id]
