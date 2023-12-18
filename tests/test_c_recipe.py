import unittest
from mc_calculator.c_crafting_block import CraftingBlock
from mc_calculator.c_recipe import Recipe


class TestRecipe(unittest.TestCase):
    def setUp(self):
        self.crafting_block = CraftingBlock("ctable3", [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.recipe_data = {
            "name": "Chest",
            "crafting_block": self.crafting_block,
            "shaped": True,
            "slots": {1: "Wood Plank", 2: "Wood Plank"},
            "ingredients": {"Wood Plank": 8},
        }

    def test_recipe_creation(self):
        recipe = Recipe(**self.recipe_data)
        self.assertEqual(recipe.name, "Chest")
        self.assertEqual(recipe.crafting_block, self.crafting_block)
        self.assertTrue(recipe.shaped)
        self.assertEqual(recipe.slots, {1: "Wood Plank", 2: "Wood Plank"})
        self.assertEqual(recipe.ingredients, {"Wood Plank": 8})

    def test_recipe_serialization(self):
        recipe = Recipe(**self.recipe_data)
        serialized = recipe.to_json()
        self.assertIsInstance(serialized, str)

    def test_recipe_deserialization(self):
        recipe = Recipe(**self.recipe_data)
        serialized = recipe.to_json()
        deserialized = Recipe.from_json(serialized)
        self.assertEqual(deserialized.name, recipe.name)
        self.assertEqual(deserialized.crafting_block.name, recipe.crafting_block.name)


if __name__ == "__main__":
    unittest.main()
