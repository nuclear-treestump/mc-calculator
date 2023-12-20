import unittest
import sqlite3
from mc_calculator.database_ops import (
    setup_database,
    save_recipe_to_db,
    fetch_recipe_by_name,
)
from mc_calculator.c_recipe import Recipe
from mc_calculator.c_crafting_block import CraftingBlock


class TestDatabaseOps(unittest.TestCase):
    def setUp(self):
        # Use an in-memory database for testing, without patching
        self.conn = sqlite3.connect(":memory:")
        setup_database(self.conn)

    def tearDown(self):
        self.conn.close()

    def test_save_and_fetch_recipe(self):
        crafting_block = CraftingBlock("ctable3", [1, 2, 3, 4, 5, 6, 7, 8, 9])
        recipe = Recipe(
            "Test Recipe",
            crafting_block,
            False,
            {},
            {"Ingredient1": 1, "Ingredient2": 2},
        )
        save_recipe_to_db(recipe, conn=self.conn)
        fetched_recipe = fetch_recipe_by_name("Test Recipe", conn=self.conn)

        self.assertIsNotNone(fetched_recipe)
        self.assertEqual(fetched_recipe.name, recipe.name)
        self.assertEqual(fetched_recipe.ingredients, recipe.ingredients)


if __name__ == "__main__":
    unittest.main()
