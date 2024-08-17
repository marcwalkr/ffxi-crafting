from database import Database
from models import Npc


class NpcRepository:
    """
    Repository class for handling NPC-related data operations.

    This class provides methods to interact with the database for retrieving
    NPC information.
    """

    _cache: dict[int, Npc] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize an NpcRepository instance.
        All NPCs are loaded into the cache on initialization.

        Args:
            db (Database): The database connection object used for querying NPC data.
        """
        self._db: Database = db
        if not NpcRepository._cache:
            self._load_npcs()

    def _load_npcs(self) -> None:
        """
        Load all NPCs into the cache.
        """
        npc_tuples = self._db.get_all_vendor_npcs()
        npcs = [Npc(*tuple) for tuple in npc_tuples]
        NpcRepository._cache.update({n.npc_id: n for n in npcs})

    def get_npc(self, npc_id: int) -> Npc | None:
        """
        Retrieve NPC information for a given NPC ID from the cache.

        Args:
            npc_id (int): The ID of the NPC to retrieve information for.

        Returns:
            Npc | None: An Npc object corresponding to the requested NPC ID,
                        or None if the NPC is not found.
        """
        if npc_id in self._cache:
            return self._cache[npc_id]
        else:
            return None
