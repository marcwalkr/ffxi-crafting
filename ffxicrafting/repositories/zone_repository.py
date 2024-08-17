from models import ZoneModel
from database import Database


class ZoneRepository:
    """
    Repository class for handling zone-related data operations.
    """

    _cache: dict[int, ZoneModel] = {}

    def __init__(self, db: Database) -> None:
        """
        Initialize a ZoneRepository instance.
        All zones are loaded into the cache on initialization.

        Args:
            db (Database): The database connection object used for querying zone data.
        """
        self._db = db
        if not ZoneRepository._cache:
            self._load_zones()

    def _load_zones(self) -> None:
        """
        Load all zones into the cache.
        """
        zone_tuples = self._db.get_all_zones()
        zones = [ZoneModel(*tuple) for tuple in zone_tuples]
        ZoneRepository._cache = zones

    def get_zone(self, zone_id: int) -> ZoneModel | None:
        """
        Retrieve a zone from the cache.
        """
        return self._cache.get(zone_id)



