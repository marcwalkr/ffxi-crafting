class Npc:
    """
    Represents a Non-Player Character (NPC) in the game.

    This class corresponds to a database table that stores information about NPCs,
    including their identifiers, names, positions, and various game-related attributes.
    """

    def __init__(self, npc_id: int, name: bytes, polutils_name: bytes, pos_rot: int, pos_x: float, pos_y: float,
                 pos_z: float, flag: int, speed: int, speed_sub: int, animation: int, animation_sub: int,
                 namevis: int, status: int, entity_flags: int, look: bytes, name_prefix: str, content_tag: str,
                 widescan: bool) -> None:
        """
        Initialize an Npc instance.

        Args:
            npc_id (int): The unique identifier for the NPC.
            name (bytes): The name of the NPC as it appears in the game.
            polutils_name (bytes): The name of the NPC as used in the POLUtils data browsing tool.
            pos_rot (int): The rotation of the NPC in its position.
            pos_x (float): The X-coordinate of the NPC's position.
            pos_y (float): The Y-coordinate of the NPC's position.
            pos_z (float): The Z-coordinate of the NPC's position.
            flag (int): A flag value associated with the NPC. Exact purpose unknown.
            speed (int): The movement speed of the NPC. Exact usage unknown.
            speed_sub (int): A sub-speed value for the NPC. Exact usage unknown.
            animation (int): An animation identifier for the NPC. Exact usage unknown.
            animation_sub (int): A sub-animation identifier for the NPC. Exact usage unknown.
            namevis (int): Possibly related to the visibility of the NPC's name. Exact usage unknown.
            status (int): The status of the NPC. Exact meaning unknown.
            entity_flags (int): Flags associated with the NPC entity. Exact meanings unknown.
            look (bytes): Data related to the NPC's appearance. Exact format unknown.
            name_prefix (str): A prefix for the NPC's name. Exact usage unknown.
            content_tag (str): A string identifying which game expansion the NPC is from.
            widescan (bool): True if the NPC can be located using the Widescan ability, False otherwise.

        Note:
            Several attributes (flag, speed, speed_sub, animation, animation_sub, namevis,
            status, entity_flags, look, name_prefix) have uncertain or unknown purposes.
            They are included for completeness as they exist in the original database schema.
        """
        self.npc_id: int = npc_id
        self.name: bytes = name
        self.polutils_name: bytes = polutils_name
        self.pos_rot: int = pos_rot
        self.pos_x: float = pos_x
        self.pos_y: float = pos_y
        self.pos_z: float = pos_z
        self.flag: int = flag
        self.speed: int = speed
        self.speed_sub: int = speed_sub
        self.animation: int = animation
        self.animation_sub: int = animation_sub
        self.namevis: int = namevis
        self.status: int = status
        self.entity_flags: int = entity_flags
        self.look: bytes = look
        self.name_prefix: str = name_prefix
        self.content_tag: str = content_tag
        self.widescan: bool = widescan
