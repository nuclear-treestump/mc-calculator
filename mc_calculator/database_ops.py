"""
This module handles database operations for the Minecraft
Recipe Calculator application, including setup and recipe management.
"""
import functools
import json
import sqlite3
from typing import Optional, Callable, List, Tuple, Any
from .recipe import Recipe

# from mc_calculator.c_crafting_block import CraftingBlock


def with_db_connection(db_path: str = "minecraft_recipes.db") -> Callable:
    """
    Open new connection if not already supplied.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper_decorator(*args: Any, **kwargs: Any) -> Any:
            # Check if 'conn' is already supplied
            conn = kwargs.get("conn")
            if conn is not None and isinstance(conn, sqlite3.Connection):
                return func(*args, **kwargs)

            # Manage a new connection
            with sqlite3.connect(db_path) as conn:
                kwargs["conn"] = conn
                return func(*args, **kwargs)

        return wrapper_decorator

    return decorator


@with_db_connection()
def setup_database(conn: Optional[sqlite3.Connection] = None) -> None:
    """
    Sets up the database for storing recipes.

    Args:
        conn (sqlite3.Connection, optional): An existing database
        connection. If not provided, a new connection will be created.
    """
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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS flags (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """
    )
    conn.commit()

    cursor.execute(
        "SELECT value FROM flags WHERE key = 'nested_recipes_migration_done'"
    )
    migration_done = cursor.fetchone()  # Check if key exists.
    if not migration_done:  # If key doesn't exist, perform migration on all recipes
        cursor.execute(
            """
        ALTER TABLE recipes
        ADD COLUMN nested_recipes_json TEXT DEFAULT '{}'
        """
        )
        conn.commit()
        migrate_nested_recipes()
        cursor.execute(
            "INSERT INTO flags (key, value) VALUES (?, ?)",
            ("nested_recipes_migration_done", "true"),
        )
        conn.commit()


@with_db_connection()
def migrate_nested_recipes(conn: Optional[sqlite3.Connection] = None) -> None:
    """
    Migrates the nested recipe data from the 'ingredients' column
    to the 'nested_recipes_json' column for all recipes.

    Args:
        conn (sqlite3.Connection, optional): An existing
        database connection. If not provided, a new connection
        will be created.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT id, ingredients FROM recipes")
    recipes = cursor.fetchall()

    for recipe_id, ingredients in recipes:
        ingredients_data = json.loads(ingredients)
        nested_recipes_json = json.dumps(ingredients_data.get("nested_recipes", {}))

        cursor.execute(
            "UPDATE recipes SET nested_recipes_json = ? WHERE id = ?",
            (nested_recipes_json, recipe_id),
        )

    conn.commit()


@with_db_connection()
def save_recipe_to_db(
    recipe: Recipe, conn: Optional[sqlite3.Connection] = None
) -> None:
    """
    Saves a recipe to the database.

    Args:
        recipe (Recipe): The recipe to be saved.
        conn (sqlite3.Connection, optional): An existing
        database connection. If not provided, a new connection
        will be created.
    """
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recipes (name, ingredients, shaped, crafting_block, output_count, nested_recipes_json) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (
            recipe.name,
            recipe.to_json(),
            recipe.shaped,
            recipe.crafting_block.name,
            recipe.output_count,
            json.dumps(recipe.nested_recipes),
        ),
    )
    conn.commit()


@with_db_connection()
def fetch_recipe_by_name(
    recipe_name: str, conn: Optional[sqlite3.Connection] = None
) -> Optional[Recipe]:
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
    cursor = conn.cursor()
    cursor.execute(
        "SELECT ingredients, nested_recipes_json FROM recipes WHERE name = ?",
        (recipe_name,),
    )
    row = cursor.fetchone()

    if row:
        return Recipe.from_json(row[0], row[1])
    return None


@with_db_connection()
def fetch_recipe_by_id(
    recipe_id: int, conn: Optional[sqlite3.Connection] = None
) -> Optional[Recipe]:
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
    cursor = conn.cursor()
    cursor.execute(
        "SELECT ingredients, nested_recipes_json FROM recipes WHERE id = ?",
        (recipe_id,),
    )
    row = cursor.fetchone()

    if row:
        return Recipe.from_json(row[0], row[1])
    return None


@with_db_connection()
def list_recipes(
    conn: Optional[sqlite3.Connection] = None,
) -> List[Tuple[int, str, int]]:
    """
    Get all recipes

    Args:
        conn (sqlite3.Connection, optional): An existing
        database connection. If not provided, a new connection
        will be created.

    Returns:
        A list of all recipes in DB
    """

    cursor = conn.cursor()
    query = "SELECT id, name, output_count FROM recipes"
    cursor.execute(query)
    recipes = cursor.fetchall()

    return [(idx + 1, recipe[1], recipe[2]) for idx, recipe in enumerate(recipes)]
