from models import ItemModel


class Item(ItemModel):
    """
    Represents a game item, extending the ItemModel with additional attributes and methods.

    This class inherits all attributes from ItemModel and adds auction-related properties.
    """

    def __init__(self, *args) -> None:
        """
        Initialize an Item instance.

        Inherits all attributes from ItemModel and initializes additional auction-related properties.

        Args:
            *args: Variable length argument list for ItemModel attributes.

        Attributes:
            single_price (float | None): The price for a single item in the auction house.
            stack_price (float | None): The price for a stack of items in the auction house.
            single_sell_freq (float | None): The sell frequency for single items.
            stack_sell_freq (float | None): The sell frequency for stacks of items.
        """
        super().__init__(*args)
        self.single_price: float | None = None
        self.stack_price: float | None = None
        self.single_sell_freq: float | None = None
        self.stack_sell_freq: float | None = None

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
        return self.sort_name.replace("_", " ").title()

    def update_from_item(self, item):
        """
        Update this Item's auction-related properties from another Item.

        Args:
            item (Item): Another Item instance to copy auction data from.
        """
        self.single_price = item.single_price
        self.stack_price = item.stack_price
        self.single_sell_freq = item.single_sell_freq
        self.stack_sell_freq = item.stack_sell_freq


class CraftableItem(Item):
    """
    Represents a craftable item in the game, extending the base Item class.

    This class adds a crafted_cost attribute to track the cost of crafting the item.
    """

    def __init__(self, *args) -> None:
        """
        Initialize a CraftableItem instance.

        Inherits all attributes from Item and initializes an additional crafted_cost property.

        Args:
            *args: Variable length argument list for Item attributes.

        Attributes:
            crafted_cost (float | None): The cost to craft this item, if applicable.
        """
        super().__init__(*args)
        self.crafted_cost: float | None = None
