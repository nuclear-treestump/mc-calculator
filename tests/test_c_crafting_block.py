import unittest
from mc_calculator.c_crafting_block import CraftingBlock


class TestCraftingBlock(unittest.TestCase):
    def test_crafting_block_creation(self):
        ctable3 = CraftingBlock("ctable3", [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertEqual(ctable3.name, "ctable3")
        self.assertEqual(ctable3.slot_layout, [1, 2, 3, 4, 5, 6, 7, 8, 9])

    def test_get_block(self):
        ctable3 = CraftingBlock("ctable3", [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.assertIs(CraftingBlock.get_block("ctable3"), ctable3)


if __name__ == "__main__":
    unittest.main()
