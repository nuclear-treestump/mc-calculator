import sqlite3
from .c_recipe import Recipe
from .c_crafting_block import CraftingBlock

def setup_database():
    conn = sqlite3.connect('minecraft_recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            shaped BOOLEAN NOT NULL,
            crafting_block TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_recipe_to_db(recipe):
    conn = sqlite3.connect('minecraft_recipes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO recipes (name, ingredients, shaped, crafting_block) VALUES (?, ?, ?, ?)', 
                   (recipe.name, recipe.to_json(), recipe.shaped, recipe.crafting_block))
    conn.commit()
    conn.close()

    while True:
        ingredient = input("Enter an ingredient (or type 'done' to finish): ")
        if ingredient.lower() == 'done':
            break
        quantity = int(input(f"Enter the quantity of {ingredient} needed: "))
        ingredients[ingredient] = quantity

    recipe = Recipe(name, crafting_block, shaped, slots, ingredients)
    save_recipe_to_db(recipe)

    return recipe

def fetch_recipe(recipe_name):
    conn = sqlite3.connect('minecraft_recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ingredients FROM recipes WHERE name = ?', (recipe_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return Recipe.from_json(row[0])
    else:
        return None