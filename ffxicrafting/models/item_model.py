class ItemModel:
    """
    Represents an item in the game.

    This class corresponds to a database table that stores basic information about
    game items. It includes data such as item identifiers, names, stack sizes,
    and various flags and categories.
    """

    def __init__(self, item_id: int, sub_id: int, name: str, sort_name: str, stack_size: int, flags: int, ah: int,
                 no_sale: bool, base_sell: int) -> None:
        """
        Initialize an Item instance.

        Args:
            item_id (int): The unique identifier for the item.
            sub_id (int): A secondary identifier for the item. Exact purpose unknown.
            name (str): The name of the item as it appears in the game.
            sort_name (str): A version of the name used for sorting purposes.
            stack_size (int): The maximum quantity of this item that can be stacked in one inventory slot.
            flags (int): A bitfield representing various item properties. Exact meanings unknown.
            ah (int): The auction house category for this item.
            no_sale (bool): True if the item cannot be sold to NPCs, False otherwise.
            base_sell (int): The base selling price of the item to NPCs.

        Note:
            The exact purposes of sub_id and flags are not fully known. They are included
            for completeness as they exist in the original database schema.
            Flags likely represent various item categories or properties used by the game code.
        """
        self.item_id: int = item_id
        self.sub_id: int = sub_id
        self.name: str = name
        self.sort_name: str = sort_name
        self.stack_size: int = stack_size
        self.flags: int = flags
        self.ah: int = ah
        self.no_sale: bool = no_sale
        self.base_sell: int = base_sell
