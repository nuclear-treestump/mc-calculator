from . import c_recipe as rcp
import math
from . import database_ops as db


def create_recipe():
    """
    Creates a new recipe by prompting the user for inputs.

    The function allows the user to enter details of a new recipe, including name, crafting block,
    output count, shape, ingredients, and nested recipes. It then saves this recipe to the database.

    Returns:
        rcp.Recipe: An instance of the Recipe class with the entered recipe details.
    """
    name = input("Enter the name of the item (e.g., Aqueous Accumulator): ")
    crafting_block = "ctable3"  # Default or choose from available blocks
    rec_output_count = int(
        input("Enter the number of items produced by this recipe (default 1): ") or "1"
    )
    shaped = input("Is the recipe shaped? (yes/no): ").lower() == "yes"

    slots = {}  # Add logic for slot-based recipes if needed
    ingredients = {}
    nested_recipes = {}

    existing_recipes = db.list_recipes()  # Retrieve existing recipes from the database

    while True:
        choice = input("Add ingredient (1) or use existing recipe (2) or 'done': ")
        if choice == "done":
            break
        elif choice == "1":
            ingredient = input("Enter an ingredient: ")
            quantity = int(input(f"Enter the quantity of {ingredient} needed: "))
            ingredients[ingredient] = quantity
        elif choice == "2":
            if existing_recipes:
                for recipe_id, recipe_name, output_count in existing_recipes:
                    print(f"{recipe_id}. {recipe_name} (makes {output_count})")
                selected_recipe_id = int(
                    input("Select the ID of the recipe to use as an ingredient: ")
                )
                # Find the selected recipe details
                selected_recipe = next(
                    (
                        name
                        for id, name, count in existing_recipes
                        if id == selected_recipe_id
                    ),
                    None,
                )
                if selected_recipe:
                    final_quantity_needed = int(
                        input(f"Enter the quantity of {selected_recipe} needed: ")
                    )
                    nested_recipes[selected_recipe_id] = final_quantity_needed
                else:
                    print("Invalid recipe ID.")
            else:
                print("No existing recipes available.")

    recipe = rcp.Recipe(
        name=name,
        crafting_block=crafting_block,
        output_count=int(rec_output_count),
        shaped=shaped,
        slots=slots,
        ingredients=ingredients,
        nested_recipes=nested_recipes,
    )
    db.save_recipe_to_db(recipe)
    return recipe


def calculate_ingredients(recipe_name, desired_quantity):
    """
    Calculates the ingredients required for a given recipe and quantity.

    This function takes a recipe name and the desired quantity of the final product, then calculates
    the total amount of each ingredient needed. It handles both simple and nested recipes.

    Args:
        recipe_name (str): The name of the recipe for which ingredients are to be calculated.
        desired_quantity (int): The desired quantity of the final product.

    Returns:
        None: This function prints the required ingredients and their quantities to the console.
    """

    def calculate(recipe, multiplier):
        ingredients_needed = {}
        steps = []

        # Calculate ingredients for the base recipe
        for ingredient, quantity in recipe.ingredients.items():
            total_quantity = quantity * multiplier
            ingredients_needed[ingredient] = (
                ingredients_needed.get(ingredient, 0) + total_quantity
            )

        # Calculate ingredients for nested recipes
        for nested_id, final_quantity_needed in recipe.nested_recipes.items():
            nested_recipe = db.fetch_recipe_by_id(nested_id)
            if nested_recipe:
                nested_multiplier = math.ceil(
                    final_quantity_needed / nested_recipe.output_count
                )
                nested_ingredients, nested_steps = calculate(
                    nested_recipe, nested_multiplier
                )
                steps.append(
                    (
                        nested_recipe.name,
                        nested_multiplier,
                        nested_recipe.output_count,
                        nested_steps,
                    )
                )
                for ing, qty in nested_ingredients.items():
                    ingredients_needed[ing] = ingredients_needed.get(ing, 0) + qty

        return ingredients_needed, steps

    def print_steps(steps):
        for step_name, step_multiplier, step_output, nested_steps in steps:
            print(
                f"- {step_multiplier} Recipe {step_name} (Output: {step_output}, "
                + ", ".join(
                    [
                        f"{qty} {ing}"
                        for ing, qty in db.fetch_recipe(step_name).ingredients.items()
                    ]
                )
                + ")"
            )
            print_steps(nested_steps)  # Recursively print nested steps

    recipe = db.fetch_recipe(recipe_name)
    if recipe:
        print(f"\nTo make {desired_quantity} {recipe.name}(s), you need to first make:")
        total_ingredients, steps = calculate(recipe, desired_quantity)
        print_steps(steps)
        print("\nTotal:")
        for ingredient, quantity in total_ingredients.items():
            print(f"- {quantity} {ingredient}")
    else:
        print("Recipe not found.")


def list_all_recipes():
    """
    Lists all the recipes currently stored in the database.

    Retrieves and displays a list of all recipes, including their name and output count,
    from the database. This function is intended for use within the main application menu.
    """
    existing_recipes = db.list_recipes()
    print("\nAvailable Recipes:")
    for recipe_number, recipe_name, output_count in existing_recipes:
        print(f"{recipe_number}. {recipe_name} (Output: {output_count})")


def select_and_calculate_recipe():
    """
    Prompts the user to select a recipe and calculates the required ingredients.

    First, it displays a list of available recipes. Then, it prompts the user to select one
    and specify the desired quantity of the final product. It calculates and displays the
    required ingredients and their quantities.
    """
    recipes = db.list_recipes()
    if recipes:
        for recipe_number, recipe_name, output_count in recipes:
            print(f"{recipe_number}. {recipe_name} (Output: {output_count})")
        recipe_choice = int(input("Enter the number of the recipe to calculate: "))
        if 1 <= recipe_choice <= len(recipes):
            recipe_id, recipe_name, _ = recipes[recipe_choice - 1]
            desired_quantity = int(
                input(f"Enter the number of {recipe_name}s you want to make: ")
            )
            calculate_ingredients(recipe_name, desired_quantity)
        else:
            print("Invalid recipe number.")
