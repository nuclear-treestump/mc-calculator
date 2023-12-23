"""
This module defines the CraftingBlock class, which is used to represent
different types of crafting blocks with specific slot layouts.
"""


class CraftingBlock:
    """
    Represents a crafting block with a specified layout.

    Attributes:
        name (str): The name of the crafting block.
        slot_layout (list): A list representing the layout of slots in the crafting block.

    Methods:
        get_block(name): Retrieves a CraftingBlock instance by its name.
    """

    _registry = {}

    def __init__(self, name, slot_layout):
        self.name = name
        self.slot_layout = slot_layout
        CraftingBlock._registry[name] = self

    @staticmethod
    def get_block(name):
        """
        Get block type from registry by name.

        Args:
            name (str): Name of the block.

        Returns:
            Recipe: CraftingBlock object from registry
        """
        return CraftingBlock._registry.get(name)


# Register crafting blocks
ctable3 = CraftingBlock("ctable3", [1, 2, 3, 4, 5, 6, 7, 8, 9])
# Add other crafting blocks as needed
