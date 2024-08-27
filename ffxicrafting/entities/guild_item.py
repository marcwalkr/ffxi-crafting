from models.guild_shop import GuildShop
from models.guild_vendor import GuildVendor
from entities.npc import Npc


class GuildItem(GuildShop, GuildVendor):
    """
    Represents a guild item in the game, combining data from GuildShop and GuildVendor.
    """

    def __init__(self, guild_id: int, item_id: int, min_price: int, max_price: int, daily_increase: int,
                 initial_quantity: int, category: str, npc_id: int, npc: Npc) -> None:
        """
        Initialize a GuildItem instance.

        Inherits all attributes from GuildShop and GuildVendor and initializes additional properties
        for managing guild information.

        Args:
            guild_id (int): The ID of the guild selling this item.
            item_id (int): The ID of the item being sold.
            min_price (int): The minimum price of the item in the guild shop.
            max_price (int): The maximum price of the item in the guild shop.
            daily_increase (int): The daily increase in the item's stock in the guild shop.
            initial_quantity (int): The initial stock quantity when the guild shop is restocked.
            category (str): The category of the guild. Must be one of:
                            Alchemy, Bonecraft, Clothcraft, Cooking, Fishing, Goldsmithing,
                            Leathercraft, Smithing, Woodworking, or Tenshodo.
            npc_id (int): The ID of the NPC vendor selling this item.
            npc (Npc): The NPC vendor selling this item.

        Attributes:
            npc (Npc): The NPC vendor selling this item.
        """
        GuildShop.__init__(guild_id, item_id, min_price, max_price, daily_increase, initial_quantity)
        GuildVendor.__init__(guild_id, npc_id, category)

        self.npc: Npc = npc
