import sqlite3
import json
import modules.c_crafting_block
import modules.c_recipe
import modules.databaseOps as db

class Recipe:
    def __init__(self, name, crafting_block="ctable3", shaped=False, slots=None, ingredients=None):
        self.name = name
        self.crafting_block = crafting_block
        self.shaped = shaped
        self.slots = slots if slots else {}
        self.ingredients = ingredients if ingredients else {}

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        return Recipe(name=data['name'], crafting_block=data['crafting_block'], 
                      shaped=data['shaped'], slots=data['slots'], ingredients=data['ingredients'])
def create_recipe():
    name = input("Enter the name of the item (e.g., Chest): ")
    shaped = input("Is the recipe shaped? (yes/no): ").lower() == 'yes'
    crafting_block = "ctable3"  # Will add stuff here later.

    slots = {} 
    ingredients = {}

def calculate_ingredients(recipe_name, desired_quantity):
    recipe = db.fetch_recipe(recipe_name)
    if recipe:
        print(f"\nTo make {desired_quantity} {recipe.name}(s), you need:")
        for ingredient, quantity in recipe.ingredients.items():
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
    db.setup_database() 
    main()
