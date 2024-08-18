from models import NpcModel
from entities import Zone


class Npc(NpcModel):
    """
    Represents a Non-Player Character (NPC) in the game.
    """

    def __init__(self, npc_id: int, polutils_name: str, zone: Zone, coordinates: str) -> None:
        """
        Initialize an Npc instance.

        Inherits all attributes from NpcModel.

        Args:
            npc_id (int): The unique identifier for the NPC.
            polutils_name (str): The name of the NPC as used in the POLUtils data browsing tool.
            zone (Zone): The zone in which the NPC is located.
            coordinates (str): The coordinates inside of the zone where the NPC is located.

        Attributes:
            name (str): The name of the NPC.
            zone (Zone): The zone in which the NPC is located.
            coordinates (str): The coordinates inside of the zone where the NPC is located.
        """
        super().__init__(npc_id, polutils_name)
        self.name: str = polutils_name
        self.zone: Zone = zone
        self.coordinates: str = coordinates
