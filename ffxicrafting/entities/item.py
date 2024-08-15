from __future__ import annotations
from typing import TYPE_CHECKING
from models import ItemModel

if TYPE_CHECKING:
    from entities import AuctionData


class Item(ItemModel):
    """
    Represents a game item, extending the ItemModel with additional attributes and methods.
    """

    def __init__(self, item_id: int, name: str, sort_name: str, stack_size: int,
                 single_auction_data: AuctionData | None, stack_auction_data: AuctionData | None,
                 min_vendor_cost: float | None, min_guild_cost: float | None) -> None:
        """
        Initialize an Item instance.

        Inherits all attributes from ItemModel and initializes additional price-related properties.

        Args:
            item_id (int): The unique identifier for the item.
            name (str): The name of the item as it appears in the game.
            sort_name (str): A version of the name used for sorting purposes.
            stack_size (int): The maximum quantity of this item that can be stacked in one inventory slot.
            single_auction_data (AuctionData | None): The auction data for a single item.
            stack_auction_data (AuctionData | None): The auction data for a stack of items.
            min_vendor_cost (float | None): The minimum cost of the item from vendors.
            min_guild_cost (float | None): The minimum cost of the item from guild shops.

        Attributes:
            min_single_price (float | None): The minimum price of the item from the auction house.
            max_single_price (float | None): The maximum price of the item from the auction house.
            average_single_price (float | None): The average price of the item from the auction house.
            single_sell_frequency (float | None): The sell frequency of the item from the auction house.
            min_stack_price (float | None): The minimum price of the item from the auction house.
            max_stack_price (float | None): The maximum price of the item from the auction house.
            average_stack_price (float | None): The average price of the item from the auction house.
            stack_sell_frequency (float | None): The sell frequency of the item from the auction house.
            min_vendor_cost (float | None): The minimum cost of the item from vendors.
            min_guild_cost (float | None): The minimum cost of the item from guild shops.
        """
        super().__init__(item_id, name, sort_name, stack_size)
        self.min_single_price: float | None = None
        self.max_single_price: float | None = None
        self.average_single_price: float | None = None
        self.single_sell_frequency: float | None = None

        if single_auction_data:
            self.min_single_price = single_auction_data.min_price
            self.max_single_price = single_auction_data.max_price
            self.average_single_price = single_auction_data.average_price
            self.single_sell_frequency = single_auction_data.sell_frequency

        self.min_stack_price: float | None = None
        self.max_stack_price: float | None = None
        self.average_stack_price: float | None = None
        self.stack_sell_frequency: float | None = None

        if stack_auction_data:
            self.min_stack_price = stack_auction_data.min_price
            self.max_stack_price = stack_auction_data.max_price
            self.average_stack_price = stack_auction_data.average_price
            self.stack_sell_frequency = stack_auction_data.sell_frequency

        self.min_vendor_cost: float | None = min_vendor_cost
        self.min_guild_cost: float | None = min_guild_cost

    def __eq__(self, __value: object) -> bool:
        """
        Check if this Item is equal to another object.

        Two Items are considered equal if they have the same item_id.

        Args:
            __value (object): The object to compare with this Item.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if isinstance(__value, Item):
            return self.item_id == __value.item_id
        return False

    def __hash__(self) -> int:
        """
        Generate a hash value for this Item.

        The hash is based on the item_id, allowing Items to be used in sets and as dictionary keys.

        Returns:
            int: The hash value of the Item.
        """
        return hash(self.item_id)

    def get_formatted_name(self):
        """
        Get a formatted version of the item's name.

        Returns:
            str: The item's name with underscores replaced by spaces and title-cased.
        """
        return self.name.replace("_", " ").title()

    def get_formatted_sort_name(self):
        """
        Get a formatted version of the item's sort name.

        Returns:
            str: The item's sort name with underscores replaced by spaces and title-cased.
        """
        return self.sort_name.replace("_", " ").title()

    def get_min_cost(self) -> int | float | None:
        """
        Calculate the minimum cost of the item from various sources.

        Returns:
            int | float | None: The lowest cost among vendor cost, guild cost, single price,
            and stack price (divided by stack size). Returns None if no valid costs are available.
        """
        if self.min_stack_price is not None:
            cost_from_stack = self.min_stack_price / self.stack_size
        else:
            cost_from_stack = None

        costs = [self.min_vendor_cost, self.min_guild_cost, self.min_single_price, cost_from_stack]
        valid_costs = [cost for cost in costs if cost is not None]

        return min(valid_costs, default=None)

    def get_max_sell_frequency(self) -> float | None:
        """
        Get the maximum sell frequency of the item.

        Returns:
            float | None: The maximum sell frequency, or None if both frequencies are None.
        """
        frequencies = [self.single_sell_frequency, self.stack_sell_frequency]
        valid_frequencies = [f for f in frequencies if f is not None]
        return max(valid_frequencies) if valid_frequencies else None

    def get_fastest_selling_price_per_unit(self) -> float | None:
        """
        Get the fastest selling price per unit of the item.
        If the stack sells faster, return the stack price divided by the stack size.
        Otherwise, return the single price. 

        Returns:
            float | None: The fastest selling price per unit of the item.

        """
        if self.single_sell_frequency is None and self.stack_sell_frequency is None:
            return None

        if self.single_sell_frequency is None:
            return self.min_stack_price / self.stack_size if self.min_stack_price is not None else None

        if self.stack_sell_frequency is None:
            return self.min_single_price

        if self.single_sell_frequency >= self.stack_sell_frequency:
            return self.min_single_price
        else:
            return self.min_stack_price / self.stack_size if self.min_stack_price is not None else None
