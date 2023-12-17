import sqlite3
import ast

def setup_database():
    conn = sqlite3.connect('minecraft_recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            ingredients TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

setup_database()

def create_recipe():
    recipe = {
        "name": input("Enter the name of the item (e.g., Chest): "),
        "ingredients": {}
    }

    while True:
        ingredient = input("Enter an ingredient (or type 'done' to finish): ")
        if ingredient.lower() == 'done':
            break
        quantity = int(input(f"Enter the quantity of {ingredient} needed: "))
        recipe["ingredients"][ingredient] = quantity

    ingredients_str = str(recipe["ingredients"])

    conn = sqlite3.connect('minecraft_recipes.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO recipes (name, ingredients) VALUES (?, ?)', 
                   (recipe["name"], ingredients_str))
    conn.commit()
    conn.close()

    return recipe

def fetch_recipes():
    conn = sqlite3.connect('minecraft_recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, ingredients FROM recipes')
    rows = cursor.fetchall()
    for row in rows:
        print(f"Name: {row[0]}, Ingredients: {row[1]}")
    conn.close()

def calculate_ingredients(recipe_name, desired_quantity):
    conn = sqlite3.connect('minecraft_recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT ingredients FROM recipes WHERE name = ?', (recipe_name,))
    row = cursor.fetchone()
    conn.close()

    if row:
        ingredients_str = row[0]
        ingredients = ast.literal_eval(ingredients_str)  # Convert string back to dictionary

        print(f"\nFor {desired_quantity} {recipe_name}(s), you need:")
        for ingredient, quantity in ingredients.items():
            total_quantity = quantity * desired_quantity
            print(f"- {total_quantity} {ingredient}")
    else:
        print("Recipe not found.")

def list_recipes():
    conn = sqlite3.connect('minecraft_recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM recipes')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("\nAvailable Recipes:")
        for idx, (recipe_id, name) in enumerate(rows, start=1):
            print(f"{idx}. {name}")
        return rows
    else:
        print("No recipes available.")
        return []

def main():
    while True:
        print("\nOptions:")
        print("1. Create a new recipe")
        print("2. List all recipes")
        print("3. Calculate ingredients for a recipe")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            create_recipe()
        elif choice == "2":
            list_recipes()
        elif choice == "3":
            recipes = list_recipes()
            if recipes:
                recipe_choice = int(input("Enter the number of the recipe to calculate: "))
                if 1 <= recipe_choice <= len(recipes):
                    recipe_id, recipe_name = recipes[recipe_choice - 1]
                    desired_quantity = int(input(f"Enter the number of {recipe_name}s you want to make: "))
                    calculate_ingredients(recipe_name, desired_quantity)
                else:
                    print("Invalid recipe number.")
        elif choice == "4":
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    setup_database() 
    main()
