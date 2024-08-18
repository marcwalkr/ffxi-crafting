class VendorLocation:
    """
    Represents the location of a vendor NPC in the game.

    This class corresponds to a database table that stores information about
    the locations of vendor NPCs within the game world, using the game's
    zone-based grid coordinate system.
    """

    def __init__(self, npc_id: int, zone_id: str, coordinates: str) -> None:
        """
        Initialize a VendorLocation instance.

        Args:
            npc_id (int): The unique identifier for the NPC vendor.
            zone_id (str): The unique identifier for the zone where the vendor is located.
            coordinates (str): The grid coordinates of the vendor within the zone.
        """
        self.npc_id: int = npc_id
        self.zone_id: str = zone_id
        self.coordinates: str = coordinates
