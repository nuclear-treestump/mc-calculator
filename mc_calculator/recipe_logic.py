"""
This module contains the logic for creating and calculating recipes
in the Minecraft Recipe Calculator application.
"""
import math
from . import c_recipe as rcp
from . import database_ops as db


def get_ingredient_input():
    """
    Prompts the user to input an ingredient and its quantity.

    Returns:
        tuple: A tuple containing the ingredient name and quantity.
    """
    ingredient = input("Enter an ingredient: ")
    quantity = int(input(f"Enter the quantity of {ingredient} needed: "))
    return ingredient, quantity


def get_nested_recipe_input(existing_recipes):
    """
    Prompts the user to select an existing recipe to use as a nested recipe.

    Args:
        existing_recipes (list): A list of existing recipes to choose from.

    Returns:
        tuple: A tuple containing the selected recipe ID and the quantity needed.
    """
    for recipe_id, recipe_name, output_count in existing_recipes:
        print(f"{recipe_id}. {recipe_name} (makes {output_count})")
    selected_recipe_id = int(
        input("Select the ID of the recipe to use as an ingredient: ")
    )
    final_quantity_needed = int(
        input(f"Enter the quantity of recipe ID {selected_recipe_id} needed: ")
    )
    return selected_recipe_id, final_quantity_needed


def create_recipe():
    """
    Creates a new recipe by prompting the user for inputs.

    This function allows the user to enter details of a new recipe,
    including its name, crafting block, output count, whether it's shaped,
    and its ingredients (including nested recipes). The new recipe
    is then saved to the database.

    Returns:
        rcp.Recipe: An instance of the Recipe class with the entered recipe details.
    """
    name = input("Enter the name of the item (e.g., Aqueous Accumulator): ")
    crafting_block = "ctable3"  # Default or choose from available blocks
    rec_output_count = int(
        input("Enter the number of items produced by this recipe (default 1): ") or "1"
    )
    shaped = input("Is the recipe shaped? (yes/no): ").lower() == "yes"

    slots = {}  # Logic for slot-based recipes if needed
    ingredients = {}
    nested_recipes = {}

    existing_recipes = db.list_recipes()  # Retrieve existing recipes from the database

    while True:
        choice = input("Add ingredient (1) or use existing recipe (2) or 'done': ")
        if choice == "done":
            break
        if choice == "1":
            ingredient, quantity = get_ingredient_input()
            ingredients[ingredient] = quantity
        elif choice == "2" and existing_recipes:
            selected_recipe_id, final_quantity_needed = get_nested_recipe_input(
                existing_recipes
            )
            nested_recipes[selected_recipe_id] = final_quantity_needed

    recipe = rcp.Recipe(
        name=name,
        crafting_block=crafting_block,
        output_count=rec_output_count,
        shaped=shaped,
        slots=slots,
        ingredients=ingredients,
        nested_recipes=nested_recipes,
    )
    db.save_recipe_to_db(recipe)
    return recipe


def calculate(recipe, desired_quantity):
    """
    Calculates the ingredients and steps required for a given recipe and quantity.

    Args:
        recipe (Recipe): The recipe for which ingredients are to be calculated.
        desired_quantity (int): The desired quantity of the final product.

    Returns:
        dict: A dictionary of ingredients and their required quantities.
        list: A list of steps involved in making the recipe.
    """
    ingredients_needed = {}
    steps = []

    desired_runs = math.ceil(desired_quantity / recipe.output_count)
    ingredients_needed.update(calculate_single_recipe_ingredients(recipe, desired_runs))

    for nested_id, quantity_needed in recipe.nested_recipes.items():
        nested_recipe = db.fetch_recipe_by_id(nested_id)
        if nested_recipe:
            (
                nested_ings,
                nested_steps,
                runs_needed,
            ) = calculate_nested_recipe_ingredients(
                nested_recipe, quantity_needed, desired_quantity
            )
            steps.append(
                (
                    nested_recipe.name,
                    runs_needed,
                    nested_recipe.output_count,
                    nested_steps,
                )
            )
            for ing, qty in nested_ings.items():
                ingredients_needed[ing] = ingredients_needed.get(ing, 0) + qty

    return ingredients_needed, steps


def calculate_single_recipe_ingredients(recipe, desired_runs):
    """
    Calculates the ingredients required for a given recipe based on the number of desired runs.

    Args:
        recipe (Recipe): The recipe for which ingredients are needed.
        desired_runs (int): The number of times the recipe needs to be executed.

    Returns:
        dict: A dictionary of ingredients and their required quantities.
    """
    ingredients_needed = {}
    for ingredient, quantity in recipe.ingredients.items():
        total_quantity = quantity * desired_runs
        ingredients_needed[ingredient] = (
            ingredients_needed.get(ingredient, 0) + total_quantity
        )
    return ingredients_needed


def calculate_nested_recipe_ingredients(
    nested_recipe, quantity_needed, desired_quantity
):
    """
    Calculates the ingredients required for nested recipes.

    Args:
        nested_recipe (Recipe): The nested recipe.
        quantity_needed (int): The quantity of the nested recipe required.
        desired_quantity (int): The desired quantity of the final product.

    Returns:
        tuple[dict, list, int]: A tuple containing the dictionary of
        ingredients/quantities, a list of steps,
        and the number of runs needed for a nested recipe
    """
    runs_needed = math.ceil(
        quantity_needed * desired_quantity / nested_recipe.output_count
    )
    nested_ingredients, nested_steps = calculate(nested_recipe, runs_needed)
    return nested_ingredients, nested_steps, runs_needed


def print_steps(steps):
    """
    Recursively prints the steps and ingredients required for a recipe and its nested recipes.

    Args:
        steps (list): A list of tuples containing details about each recipe step.
                      Each tuple contains the recipe name, the number of runs needed,
                      the output count, and any nested steps.
    """
    for step_name, step_multiplier, step_output, nested_steps in steps:
        nested_recipe = db.fetch_recipe_by_name(step_name)
        print(
            f"- {step_multiplier} Recipe {step_name} (Output: {step_output}, "
            + ", ".join(
                [f"{qty} {ing}" for ing, qty in nested_recipe.ingredients.items()]
            )
            + ")"
        )
        print_steps(nested_steps)  # Recursively print nested steps


def calculate_ingredients(recipe_name, desired_quantity):
    """
    Calculates the ingredients required for a given recipe and quantity.

    Args:
        recipe_name (str): The name of the recipe for which ingredients are to be calculated.
        desired_quantity (int): The desired quantity of the final product.

    Returns:
        None: This function prints the required ingredients and their quantities to the console.
    """
    recipe = db.fetch_recipe_by_name(recipe_name)
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
            _, recipe_name, _ = recipes[recipe_choice - 1]
            desired_quantity = int(
                input(f"Enter the number of {recipe_name}s you want to make: ")
            )
            calculate_ingredients(recipe_name, desired_quantity)
        else:
            print("Invalid recipe number.")
