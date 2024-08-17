from models import ZoneModel


class Zone(ZoneModel):
    """
    Represents a zone in the game.
    Subclasses ZoneModel and adds additional formatting to the zone name.
    """

    def __init__(self, zone_id: int, name: str) -> None:
        """
        Initialize a Zone instance.
        Formats the zone name by replacing underscores with spaces.

        Args:
            zone_id (int): The ID of the zone.
            name (str): The name of the zone.
        """
        super().__init__(zone_id, name)
        self.name = name.replace("_", " ")
