from models import ZoneModel


class Zone(ZoneModel):
    """
    Represents a zone in the game.
    Subclasses ZoneModel and adds additional formatting to the zone name.
    """

    def __init__(self, zone_id: int, name: str) -> None:
        """
        Initialize a Zone instance.
        """
        super().__init__(zone_id, name)
        self.name = name.replace("_", " ")
