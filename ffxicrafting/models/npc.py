class Npc:
    """
    Represents a Non-Player Character (NPC) in the game.

    This class corresponds to a database table that stores information about NPCs,
    used to retrieve the NPC's name.
    """

    def __init__(self, npc_id: int, polutils_name: str) -> None:
        """
        Initialize an Npc instance.

        Args:
            npc_id (int): The unique identifier for the NPC.
            polutils_name (str): The name of the NPC as used in the POLUtils data browsing tool.
        """
        self.npc_id: int = npc_id
        self.polutils_name: str = polutils_name
