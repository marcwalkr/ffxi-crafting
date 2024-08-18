from database import Database
from models import NpcModel


class NpcRepository:
    """
    Repository class for handling NPC-related data operations.

    This class provides methods to interact with the database for retrieving
    vendor NPC information.
    """

    _cache: list[NpcModel] = []

    def __init__(self, db: Database) -> None:
        """
        Initialize an NpcRepository instance.
        All vendor NPCs are loaded into the cache on initialization.

        Args:
            db (Database): The database connection object used for querying NPC data.
        """
        self._db: Database = db
        if not NpcRepository._cache:
            self._load_npcs()

    def _load_npcs(self) -> None:
        """
        Load all vendor NPCs into the cache.
        """
        npc_tuples = self._db.get_all_vendor_npcs()
        npcs = [NpcModel(*tuple) for tuple in npc_tuples]
        NpcRepository._cache = npcs

    def get_all_npcs(self) -> list[NpcModel]:
        """
        Retrieve all vendor NPC information from the cache.

        Returns:
            list[NpcModel]: A list of NpcModel objects.
        """
        return self._cache
    
    def delete_cache(self) -> None:
        """
        Delete the cache.
        """
        self._cache = []

