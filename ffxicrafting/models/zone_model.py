class ZoneModel:
    """
    Represents a zone in the game.

    This class corresponds to a database table that contains the zone information.
    """

    def __init__(self, zone_id: int, name: str) -> None:
        """
        Initialize a ZoneModel instance.

        Args:
            zone_id (int): The unique identifier for the zone.
            name (str): The name of the zone.
        """
        self.zone_id: int = zone_id
        self.name: str = name
