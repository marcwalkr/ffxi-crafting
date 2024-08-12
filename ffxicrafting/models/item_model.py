class ItemModel:
    """
    Represents an item in the game.

    This class corresponds to a database table that stores basic information about
    game items. It includes data such as item identifiers, names and stack sizes.
    """

    def __init__(self, item_id: int, name: str, sort_name: str, stack_size: int) -> None:
        """
        Initialize an Item instance.

        Args:
            item_id (int): The unique identifier for the item.
            name (str): The name of the item as it appears in the game.
            sort_name (str): A version of the name used for sorting purposes.
            stack_size (int): The maximum quantity of this item that can be stacked in one inventory slot.

        Note:
            The exact purposes of sub_id and flags are not fully known. They are included
            for completeness as they exist in the original database schema.
            Flags likely represent various item categories or properties used by the game code.
        """
        self.item_id: int = item_id
        self.name: str = name
        self.sort_name: str = sort_name
        self.stack_size: int = stack_size
