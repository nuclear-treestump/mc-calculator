"""
This module contains the logic for creating and calculating recipes
in the Minecraft Recipe Calculator application.
"""
import logging
import math
from typing import List, Tuple, Dict
from . import database_ops as db
from .decorator import auto_log
from . import recipe as rcp
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)


@auto_log(__name__)
def get_ingredient_input() -> Tuple[str, int]:
    """
    Prompts the user to input an ingredient and its quantity.

    Returns:
        tuple: A tuple containing the ingredient name and quantity.
    """
    while True:
        ingredient = input("Enter an ingredient: ")
        logger.info(f"User entered ingredient: {ingredient}")
        if 0 < len(ingredient) <= 50:  # Check for a reasonable length
            logger.info(f"User ingredient {ingredient} accepted.")
            break
        logger.warning(f"Invalid ingredient input length. Length: {len(ingredient)}")
        print("Invalid input. Please enter a valid ingredient name.")

    while True:
        try:
            quantity = int(input(f"Enter the quantity of {ingredient} needed: "))
            if quantity > 0:  # Ensure quantity is positive
                break
            print("Quantity must be positive.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for quantity.")

    return ingredient, quantity


@auto_log(__name__)
def get_nested_recipe_input(
    existing_recipes: List[Tuple[int, str, int]]
) -> Tuple[int, int]:
    """
    Prompts the user to select an existing recipe to use as a nested recipe.

    Args:
        existing_recipes (list): A list of existing recipes to choose from.

    Returns:
        tuple: A tuple containing the selected recipe ID and the quantity needed.
    """
    while True:
        try:
            list_all_recipes()
            selected_recipe_id = int(
                input("Select the ID of the recipe to use as an ingredient: ")
            )
            logger.info(f"User selected recipe ID: {selected_recipe_id}")
            if any(
                recipe_id == selected_recipe_id for recipe_id, _, _ in existing_recipes
            ):
                logger.debug(f"Successfully selected recipe ID: {selected_recipe_id}")
                break
            logger.warning(f"User selected invalid recipe ID: {selected_recipe_id}")
            print("Invalid ID. Please select a valid recipe ID.")
        except ValueError:
            print("Invalid input. Please enter a valid integer for the recipe ID.")
    final_quantity_needed = int(
        input(f"Enter the quantity of recipe ID {selected_recipe_id} needed: ")
    )
    return selected_recipe_id, final_quantity_needed


@auto_log(__name__)
def create_recipe() -> rcp.Recipe:
    """
    Creates a new recipe by prompting the user for inputs.

    This function allows the user to enter details of a new recipe,
    including its name, crafting block, output count, whether it's shaped,
    and its ingredients (including nested recipes). The new recipe
    is then saved to the database.

    Returns:
        rcp.Recipe: An instance of the Recipe class with the entered recipe details.
    """
    logger.info("Starting new recipe creation")
    while True:
        name = input("Enter the name of the item (e.g., Aqueous Accumulator): ")
        logger.info(f"User entered Recipe Name: {name}")
        if 0 < len(name) <= 50:  # Check for a reasonable length
            logger.debug(f"Recipe name: '{name}' accepted.")
            break
        logger.warning(f"User recipe name rejected. Length: {len(name)}")
        print("Invalid input. Please enter a valid recipe name.")
    crafting_block = "ctable3"  # Default or choose from available blocks
    while True:
        try:
            rec_output_count_input = input(
                "Enter the number of items produced by this recipe (default 1): "
            )
            rec_output_count = (
                int(rec_output_count_input) if rec_output_count_input else 1
            )
            if rec_output_count > 0:  # Check for a positive integer
                break
            print("Please enter a positive integer.")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

    while True:
        shaped = input("Is the recipe shaped? (yes/no): ").lower()[:3]
        if shaped in ("yes", "y", "t", "1"):
            break
        if shaped in ("no", "n", "f", "0"):
            break
        print(f"You entered: {shaped}, Invalid input.")

    slots = {}  # Logic for slot-based recipes if needed
    ingredients = {}
    nested_recipes = {}

    existing_recipes = db.list_recipes()  # Retrieve existing recipes from the database

    while True:
        choice = input("Add ingredient (1) or use existing recipe (2) or 'done': ")
        if choice in ("1", "2", "done"):
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
        print("Invalid input. Please enter '1', '2', or 'done'.")

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


@auto_log(__name__)
def calculate(
    recipe: rcp.Recipe, desired_quantity: int
) -> Tuple[Dict[str, int], List[Tuple[str, int, int, List, int]]]:
    """
    Calculates the ingredients and steps required for a given recipe and quantity.

    Args:
        recipe (Recipe): The recipe for which ingredients are to be calculated.
        desired_quantity (int): The desired quantity of the final product.

    Returns:
        dict: A dictionary of ingredients and their required quantities.
        list: A list of steps involved in making the recipe.
    """
    logger.info(
        f"Starting calculation for recipe: {recipe.name} for quantity: {desired_quantity}"
    )
    ingredients_needed = {}
    steps = []

    desired_runs = math.ceil(desired_quantity / recipe.output_count)
    ingredients_needed.update(calculate_single_recipe_ingredients(recipe, desired_runs))

    for nested_id, quantity_needed in recipe.nested_recipes.items():
        nested_recipe = db.fetch_recipe_by_id(nested_id)
        if nested_recipe:
            nested_runs = math.ceil(
                quantity_needed * desired_runs / nested_recipe.output_count
            )
            nested_ingredients = calculate_base_ingredients(nested_recipe, nested_runs)

            # Calculate the total output and waste for each nested recipe step
            total_output = nested_runs * nested_recipe.output_count
            waste = total_output - (quantity_needed * desired_runs)

            steps.append(
                (nested_recipe.name, nested_runs, nested_recipe.output_count, [], waste)
            )

            for ing, qty in nested_ingredients.items():
                ingredients_needed[ing] = ingredients_needed.get(ing, 0) + qty

    return ingredients_needed, steps


@auto_log(__name__)
def calculate_single_recipe_ingredients(
    recipe: rcp.Recipe, desired_runs: int
) -> Dict[str, int]:
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
        logger.info(f"Calculating {ingredient} with quantity {quantity}")
        total_quantity = quantity * desired_runs
        ingredients_needed[ingredient] = (
            ingredients_needed.get(ingredient, 0) + total_quantity
        )
    return ingredients_needed


@auto_log(__name__)
def calculate_nested_recipe_ingredients(
    nested_recipe: rcp.Recipe, quantity_needed: int, desired_quantity: int
) -> Tuple[Dict[str, int], List, int]:
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
    logger.info(
        f"Starting calculation for {nested_recipe.name}, quantity needed: {quantity_needed}, desired quantity: {desired_quantity}"
    )
    runs_needed = math.ceil(
        quantity_needed * desired_quantity / nested_recipe.output_count
    )
    nested_ingredients, nested_steps = calculate(nested_recipe, runs_needed)
    return nested_ingredients, nested_steps, runs_needed


@auto_log(__name__)
def calculate_base_ingredients(recipe: rcp.Recipe, runs_needed: int) -> Dict[str, int]:
    base_ingredients = {}
    for ingredient, quantity in recipe.ingredients.items():
        base_ingredients[ingredient] = (
            base_ingredients.get(ingredient, 0) + quantity * runs_needed
        )

    for nested_id, quantity_needed in recipe.nested_recipes.items():
        nested_recipe = db.fetch_recipe_by_id(nested_id)
        if nested_recipe:
            nested_runs = math.ceil(
                quantity_needed * runs_needed / nested_recipe.output_count
            )
            nested_base_ings = calculate_base_ingredients(nested_recipe, nested_runs)
            for ing, qty in nested_base_ings.items():
                base_ingredients[ing] = base_ingredients.get(ing, 0) + qty

    return base_ingredients


@auto_log(__name__)
def print_steps(steps: List[Tuple[str, int, int, List, int]]) -> None:
    """
    Recursively prints the steps and ingredients required for a recipe and its nested recipes,
    including the total output and any waste.

    Args:
        steps (list): A list of tuples containing details about each recipe step.
                      Each tuple contains the recipe name, the number of runs needed,
                      the output count, any nested steps, and the waste.
    """
    logger.info("Printing steps. . .")
    for step_name, step_multiplier, step_output, nested_steps, waste in steps:
        nested_recipe = db.fetch_recipe_by_name(step_name)
        total_output = step_multiplier * step_output
        waste_info = f", Waste: {waste}x {step_name}" if waste > 0 else "Waste: None"

        print(
            f"- {step_multiplier}x Recipe {step_name} (Total Output: {total_output} {step_name} {waste_info}, Ingredients: "
            + " ".join(
                [f"{qty} {ing}" for ing, qty in nested_recipe.ingredients.items()]
            )
            + ", "
            + " ".join(
                [
                    f"{n_qty} {db.fetch_recipe_by_id(int(n_id)).name}"
                    for n_id, n_qty in nested_recipe.nested_recipes.items()
                ]
            )
            + ")"
        )
        print_steps(nested_steps)  # Recursively print nested steps


@auto_log(__name__)
def calculate_ingredients(recipe_name: str, desired_quantity: int) -> None:
    """
    Calculates the ingredients required for a given recipe and quantity.

    Args:
        recipe_name (str): The name of the recipe for which ingredients are to be calculated.
        desired_quantity (int): The desired quantity of the final product.

    Returns:
        None: This function prints the required ingredients and their quantities to the console.
    """
    recipe = db.fetch_recipe_by_name(recipe_name)
    logger.info(f"Calculating: {recipe.name} for quantity: {desired_quantity}")
    if recipe:
        print(f"\nTo make {desired_quantity} {recipe.name}(s), you need to first make:")
        total_ingredients, steps = calculate(recipe, desired_quantity)
        print_steps(steps)
        print("\nTotal:")
        for ingredient, quantity in total_ingredients.items():
            print(f"- {quantity} {ingredient}")
    else:
        print("Recipe not found.")


@auto_log(__name__)
def list_all_recipes() -> None:
    """
    Lists all the recipes currently stored in the database.

    Retrieves and displays a list of all recipes, including their name and output count,
    from the database. This function is intended for use within the main application menu.
    """
    logger.info("Printing all recipes to console")
    existing_recipes = db.list_recipes()
    print("\nAvailable Recipes:")
    for recipe_number, recipe_name, output_count in existing_recipes:
        print(f"{recipe_number}. {recipe_name} (Output: {output_count})")


@auto_log(__name__)
def select_and_calculate_recipe() -> None:
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

        while True:
            list_all_recipes()
            try:
                recipe_choice = int(
                    input("Enter the number of the recipe to calculate: ")
                )
                if 1 <= recipe_choice <= len(recipes):
                    break
                print(
                    "Invalid recipe number. Please enter a number within the displayed range."
                )
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        _, recipe_name, _ = recipes[recipe_choice - 1]

        while True:
            try:
                desired_quantity = int(
                    input(f"Enter the number of {recipe_name}s you want to make: ")
                )
                if desired_quantity > 0:
                    break
                print("Invalid quantity. Please enter a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")

        calculate_ingredients(recipe_name, desired_quantity)
    else:
        print("No recipes available.")
