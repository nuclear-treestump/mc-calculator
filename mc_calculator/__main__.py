"""
This module is the entry point for the Minecraft Recipe Calculator application.

It provides a menu-driven interface for interacting with the application, enabling users to create,
list, and calculate ingredients for recipes, as well as exit the application.
"""

from . import database_ops as db
from . import recipe_logic as rl

MC_CALC_TITLE = """
      __      __             __                 ___  __   __  
|\/| /    __ /     /\  |    /    |  | |     /\   |  /  \ |__) 
|  | \__     \__  /--\ |___ \__  \__/ |___ /--\  |  \__/ |  \ 
                                                               
"""


def display_credits():
    """
    Displays the credits for the application.
    """
    print("MC-CALCULATOR created by: 0xIkari")
    print(
        "For more information, visit: https://github.com/nuclear-treestump/mc-calculator"
    )


def main():
    """
    Main function to run the Minecraft Recipe Calculator application.

    This function provides a menu-driven interface for the user to interact with the application.
    It allows users to create new recipes, list all recipes, calculate ingredients for a recipe,
    and exit the application.
    """
    print(MC_CALC_TITLE)
    while True:
        print("\nOptions:")
        print("1. Create a new recipe")
        print("2. List all recipes")
        print("3. Calculate ingredients for a recipe")
        print("4. Exit")
        print("5. Credits")
        choice = input("Choose an option: ")

        if choice == "1":
            rl.create_recipe()
        elif choice == "2":
            rl.list_all_recipes()
        elif choice == "3":
            rl.select_and_calculate_recipe()
        elif choice == "4":
            break
        elif choice == "5":
            display_credits()
        else:
            print("Invalid option.")


if __name__ == "__main__":
    db.setup_database()
    main()
