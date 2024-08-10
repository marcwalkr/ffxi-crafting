from __future__ import annotations
from typing import TYPE_CHECKING
from typing import TypeVar
from entities import CraftableItem

if TYPE_CHECKING:
    from entities import Item

ItemType = TypeVar("ItemType", bound="Item")


class Result(CraftableItem):
    """
    Represents a crafting result in the game, extending the CraftableItem class with
    additional properties and methods specific to crafting outcomes.
    """

    instances = []

    def __init__(self, *args) -> None:
        """
        Initialize a Result instance.

        Inherits all attributes from CraftableItem and initializes additional properties
        specific to crafting results.

        Args:
            *args: Variable length argument list for CraftableItem attributes.

        Attributes:
            profit_contribution (float | None): The profit contribution of this result to the total profit.
        """
        super().__init__(*args)
        self.profit_contribution: float | None = None
        Result.instances.append(self)

    @classmethod
    def get(cls, item_id: int) -> 'Result | None':
        """
        Retrieve a Result instance by its item ID.

        Args:
            item_id (int): The ID of the item to retrieve.

        Returns:
            Result | None: The Result instance with the specified item ID, or None if not found.
        """
        for result in cls.instances:
            if result.item_id == item_id:
                return result
        return None

    @classmethod
    def sync(cls, item: ItemType) -> None:
        """
        Synchronize all Result instances with updated item data.

        This method updates the auction-related attributes of all existing Result instances
        with data from a corresponding Item instance or its subclass.

        Args:
            item (ItemType): The item containing updated auction data.
        """
        for result in cls.instances:
            if result.item_id == item.item_id:
                result.update_from_item(item)

    def get_best_sell_frequency(self) -> float:
        """
        Get the best sell frequency between single and stack sales.

        Returns:
            float: The higher sell frequency between single_sell_frequency and stack_sell_frequency.
                   Returns 0 if both frequencies are None.
        """
        single_frequency = self.single_sell_frequency or 0
        stack_frequency = self.stack_sell_frequency or 0
        return max(single_frequency, stack_frequency)
