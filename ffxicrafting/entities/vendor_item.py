from config import SettingsManager
from entities import Npc
from models import VendorItemModel


class VendorItem(VendorItemModel):
    """
    Represents a vendor item in the game, extending the VendorItemModel with additional
    functionality for managing vendor information.
    """

    def __init__(self, item_id: int, npc_id: int, min_price: int, sandoria_rank: int, bastok_rank: int, windurst_rank: int,
                 sandoria_citizen: bool, bastok_citizen: bool, windurst_citizen: bool, npc: Npc) -> None:
        """
        Initialize a VendorItem instance.

        Inherits all attributes from VendorItemModel and initializes additional properties
        for managing vendor information.

        Args:
            item_id (int): The ID of the item being sold.
            npc_id (int): The ID of the NPC vendor selling this item.
            min_price (int): The minimum price of the item when purchased from this vendor.
            sandoria_rank (int): The required conquest rank for San d'Oria to sell this item.
            bastok_rank (int): The required conquest rank for Bastok to sell this item.
            windurst_rank (int): The required conquest rank for Windurst to sell this item.
            sandoria_citizen (bool): True if the buyer must be a San d'Oria citizen to purchase.
            bastok_citizen (bool): True if the buyer must be a Bastok citizen to purchase.
            windurst_citizen (bool): True if the buyer must be a Windurst citizen to purchase.

        Attributes:
            npc (Npc): The NPC vendor selling this item.
            max_price (int): The maximum price of the item when purchased from this vendor.
        """
        super().__init__(item_id, npc_id, min_price, sandoria_rank, bastok_rank, windurst_rank,
                         sandoria_citizen, bastok_citizen, windurst_citizen)

        self.npc: Npc = npc
        self.max_price = self._calculate_max_price()

    def _calculate_max_price(self) -> int:
        """
        Calculate the maximum price of the item when purchased from this vendor.
        Uses the formula from AirSkyBoat to calculate the price with fame level 1

        Returns:
            int: The maximum price of the item when purchased from this vendor.
        """
        higher_tax_areas = ["Southern San d'Oria", "Northern San d'Oria", "Port San d'Oria", "Selbina", "Rabao"]
        if self.npc.zone.name in higher_tax_areas:
            return (1 + ((7 / 45) * (9 - 1) / 8)) * self.min_price
        else:
            return (1 + (0.13 * (9 - 1) / 8)) * self.min_price

    def can_purchase(self) -> bool:
        """
        Check if the item can be purchased from this vendor.
        Checks the current conquest ranking and the vendor's rank requirement.

        Returns:
            bool: True if the item can be purchased, False otherwise.
        """
        sandoria_rank = SettingsManager.get_sandoria_rank()
        bastok_rank = SettingsManager.get_bastok_rank()
        windurst_rank = SettingsManager.get_windurst_rank()

        if (self.sandoria_rank == 0 or self.sandoria_rank >= sandoria_rank) and \
           (self.bastok_rank == 0 or self.bastok_rank >= bastok_rank) and \
           (self.windurst_rank == 0 or self.windurst_rank >= windurst_rank):
            return True
        else:
            return False


class RegionalVendorItem(VendorItem):
    """
    Represents a vendor item in the game from a regional vendor, extending VendorItem with additional
    functionality that deals with regions.
    """

    def __init__(self, item_id: int, npc_id: int, min_price: int, sandoria_rank: int, bastok_rank: int, windurst_rank: int,
                 sandoria_citizen: bool, bastok_citizen: bool, windurst_citizen: bool, npc: Npc, region: str) -> None:
        """
        Initialize a RegionalVendorItem instance.

        Inherits all attributes from VendorItem and initializes additional properties
        for managing regional vendor information.
        """
        super().__init__(item_id, npc_id, min_price, sandoria_rank, bastok_rank, windurst_rank,
                         sandoria_citizen, bastok_citizen, windurst_citizen, npc)

        self.region = region

    def can_purchase(self) -> bool:
        """
        Check if the item can be purchased from this vendor.
        Checks the region is currently controlled by beastmen.

        Returns:
            bool: True if the item can be purchased, False otherwise.
        """
        return self.region not in SettingsManager.get_beastmen_regions()
