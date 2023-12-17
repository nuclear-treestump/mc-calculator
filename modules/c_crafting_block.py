class CraftingBlock:
    _registry = {}

    def __init__(self, name, slot_layout):
        self.name = name
        self.slot_layout = slot_layout
        CraftingBlock._registry[name] = self

    @staticmethod
    def get_block(name):
        return CraftingBlock._registry.get(name)


# Register crafting blocks
ctable3 = CraftingBlock("ctable3", [1, 2, 3, 4, 5, 6, 7, 8, 9])
# Add other crafting blocks as needed
