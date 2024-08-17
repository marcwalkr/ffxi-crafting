from database import Database
from entities import Zone
from repositories import ZoneRepository


class ZoneController:
    """
    Controller class for handling zone-related data operations.
    This class provides methods to interact with zones, including retrieving zone information.
    """

    def __init__(self, db: Database) -> None:
        """
        Initialize a ZoneController instance.

        Args:
            db (Database): The database connection object.
        """
        self._zone_repository = ZoneRepository(db)

    def get_zone(self, zone_id: int) -> Zone | None:
        """
        Retrieve a zone from the cache in ZoneRepository and return it as a Zone object.

        Args:
            zone_id (int): The ID of the zone to retrieve.

        Returns:
            Zone | None: The Zone object if found, otherwise None.
        """
        zone_model = self._zone_repository.get_zone(zone_id)
        if zone_model:
            return Zone(zone_model.zone_id, zone_model.name)
        return None
