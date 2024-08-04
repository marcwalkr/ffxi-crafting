class VendorItem:
    """
    Represents an item sold by a vendor in the game.

    This class corresponds to a database table that stores information about items
    available from vendors, including pricing and purchase restrictions based on
    nation rankings and citizenship.
    """

    def __init__(self, item_id: int, npc_id: int, price: int, sandoria_rank: int, bastok_rank: int, windurst_rank: int,
                 sandoria_citizen: bool, bastok_citizen: bool, windurst_citizen: bool) -> None:
        """
        Initialize a VendorItem instance.

        Args:
            item_id (int): The unique identifier for the item being sold.
            npc_id (int): The unique identifier for the NPC vendor selling this item.
            price (int): The price of the item when purchased from this vendor.
            sandoria_rank (int): The required conquest rank for San d'Oria to sell this item.
            bastok_rank (int): The required conquest rank for Bastok to sell this item.
            windurst_rank (int): The required conquest rank for Windurst to sell this item.
            sandoria_citizen (bool): True if the buyer must be a San d'Oria citizen to purchase.
            bastok_citizen (bool): True if the buyer must be a Bastok citizen to purchase.
            windurst_citizen (bool): True if the buyer must be a Windurst citizen to purchase.

        The rank values (sandoria_rank, bastok_rank, windurst_rank) represent:
            0: The nation's rank doesn't affect the sale of this item.
            1: The nation must be in 1st place in the conquest rankings.
            2: The nation must be in 1st or 2nd place in the conquest rankings.

        The citizen boolean values indicate whether citizenship of the respective
        nation is required to purchase this item from the vendor.
        """
        self.item_id: int = item_id
        self.npc_id: int = npc_id
        self.price: int = price
        self.sandoria_rank: int = sandoria_rank
        self.bastok_rank: int = bastok_rank
        self.windurst_rank: int = windurst_rank
        self.sandoria_citizen: bool = sandoria_citizen
        self.bastok_citizen: bool = bastok_citizen
        self.windurst_citizen: bool = windurst_citizen
