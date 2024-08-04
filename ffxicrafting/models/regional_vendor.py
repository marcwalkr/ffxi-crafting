class RegionalVendor:
    """
    Represents a regional vendor NPC in the game.

    This class corresponds to a database table that stores information about regional vendors,
    linking NPCs to the specific regions they sell items for.
    """

    def __init__(self, npc_id: int, region: str) -> None:
        """
        Initialize a RegionalVendor instance.

        Args:
            npc_id (int): The unique identifier for the NPC who acts as a regional vendor.
            region (str): The name of the region this vendor sells items for.
        """
        self.npc_id: int = npc_id
        self.region: str = region
