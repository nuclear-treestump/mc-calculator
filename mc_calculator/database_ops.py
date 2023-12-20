"""
This module handles database operations for the Minecraft
Recipe Calculator application, including setup and recipe management.
"""
import sqlite3
from mc_calculator.c_recipe import Recipe

# from mc_calculator.c_crafting_block import CraftingBlock


def setup_database(conn=None):
    """
    Sets up the database for storing recipes.

    Args:
        conn (sqlite3.Connection, optional): An existing database
        connection. If not provided, a new connection will be created.
    """
    should_close = False
    if conn is None:
        conn = sqlite3.connect("minecraft_recipes.db")
        should_close = True

    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            shaped BOOLEAN NOT NULL,
            crafting_block TEXT NOT NULL,
            output_count INTEGER NOT NULL DEFAULT 1
        )
    """
    )
    conn.commit()

    if should_close:
        conn.close()


def save_recipe_to_db(recipe, conn=None):
    """
    Saves a recipe to the database.

    Args:
        recipe (Recipe): The recipe to be saved.
        conn (sqlite3.Connection, optional): An existing
        database connection. If not provided, a new connection
        will be created.
    """
    should_close = False
    if conn is None:
        conn = sqlite3.connect("minecraft_recipes.db")
        should_close = True

    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recipes (name, ingredients, shaped, crafting_block, output_count) "
        "VALUES (?, ?, ?, ?, ?)",
        (
            recipe.name,
            recipe.to_json(),
            recipe.shaped,
            recipe.crafting_block.name,
            recipe.output_count,
        ),
    )
    conn.commit()

    if should_close:
        conn.close()


def fetch_recipe(recipe_name: str, conn=None):
    """
    Get a recipe from the database by name.

    Args:
        recipe_name (str): The name of the recipe to query for.
        conn (sqlite3.Connection, optional): An existing
        database connection. If not provided, a new connection
        will be created.

    Returns:
        Recipe object
    """
    should_close = False
    if conn is None:
        conn = sqlite3.connect("minecraft_recipes.db")
        should_close = True

    cursor = conn.cursor()
    cursor.execute("SELECT ingredients FROM recipes WHERE name = ?", (recipe_name,))
    row = cursor.fetchone()

    if should_close:
        conn.close()

    if row:
        return Recipe.from_json(row[0])
    return None


def fetch_recipe_by_id(recipe_id, conn=None):
    """
    Get a recipe from the database by ID.

    Args:
        recipe_id (str): The ID of the recipe to query for.
        conn (sqlite3.Connection, optional): An existing
        database connection. If not provided, a new connection
        will be created.

    Returns:
        Recipe object
    """
    should_close = False
    if conn is None:
        conn = sqlite3.connect("minecraft_recipes.db")
        should_close = True

    cursor = conn.cursor()
    cursor.execute("SELECT ingredients FROM recipes WHERE id = ?", (recipe_id,))
    row = cursor.fetchone()

    if should_close:
        conn.close()

    if row:
        return Recipe.from_json(row[0])
    return None


def list_recipes(conn=None):
    """
    Get all recipes

    Args:
        conn (sqlite3.Connection, optional): An existing
        database connection. If not provided, a new connection
        will be created.

    Returns:
        A list of all recipes in DB
    """
    should_close = False
    if conn is None:
        conn = sqlite3.connect("minecraft_recipes.db")
        should_close = True

    cursor = conn.cursor()
    query = "SELECT id, name, output_count FROM recipes"
    cursor.execute(query)
    recipes = cursor.fetchall()

    if should_close:
        conn.close()

    return [(idx + 1, recipe[1], recipe[2]) for idx, recipe in enumerate(recipes)]
