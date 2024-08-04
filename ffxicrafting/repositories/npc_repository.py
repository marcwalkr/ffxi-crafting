from database import Database
from models import Npc


class NpcRepository:
    """
    Repository class for handling NPC-related data operations.

    This class provides methods to interact with the database for retrieving
    NPC information. It implements caching to improve performance for
    frequently accessed NPCs.
    """

    _cache: dict[int, Npc] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize an NpcRepository instance.

        Args:
            db (Database): The database connection object used for querying NPC data.
        """
        self._db: Database = db

    def get_npc(self, npc_id: int) -> Npc | None:
        """
        Retrieve NPC information for a given NPC ID.

        This method first checks the cache for the requested NPC. If not found,
        it queries the database and caches the result for future use.

        Args:
            npc_id (int): The ID of the NPC to retrieve information for.

        Returns:
            Npc | None: An Npc object corresponding to the requested NPC ID,
                        or None if the NPC is not found.
        """
        if npc_id in self._cache:
            return self._cache[npc_id]
        else:
            npc_tuple = self._db.get_npc(npc_id)
            if npc_tuple is not None:
                self._cache[npc_id] = Npc(*npc_tuple)
                return self._cache[npc_id]
            else:
                return None
