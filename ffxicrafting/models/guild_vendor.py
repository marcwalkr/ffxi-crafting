class GuildVendor:
    """
    Represents a guild vendor in the game.

    This class corresponds to a database table that connects guilds to their associated
    NPCs and specifies the guild category. It allows for looking up NPC locations and
    determining which crafting discipline or special merchant category a guild vendor
    belongs to.
    """

    def __init__(self, guild_id: int, npc_id: int, category: str) -> None:
        """
        Initialize a GuildVendor instance.

        Args:
            guild_id (int): The unique identifier for the guild.
            npc_id (int): The unique identifier for the NPC associated with this guild vendor.
            category (str): The category of the guild. Must be one of:
                            Alchemy, Bonecraft, Clothcraft, Cooking, Fishing, Goldsmithing,
                            Leathercraft, Smithing, Woodworking, or Tenshodo.

        The category specifies the type of guild or special merchant:
        - Crafting guilds: Alchemy, Bonecraft, Clothcraft, Cooking, Goldsmithing,
                           Leathercraft, Smithing, Woodworking
        - Other guilds: Fishing
        - Special merchants: Tenshodo
        """
        self.guild_id: int = guild_id
        self.npc_id: int = npc_id
        self.category: str = category
