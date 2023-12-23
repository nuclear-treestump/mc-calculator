"""
This module is the entry point for the Minecraft Recipe Calculator application.

It provides a menu-driven interface for interacting with the application, enabling users to create,
list, and calculate ingredients for recipes, as well as exit the application.
"""
import logging
from . import database_ops as db
from .decorator import auto_log
from . import recipe_logic as rl

MC_CALC_TITLE = """
      __      __             __                 ___  __   __  
|\/| /    __ /     /\  |    /    |  | |     /\   |  /  \ |__) 
|  | \__     \__  /--\ |___ \__  \__/ |___ /--\  |  \__/ |  \ 
                                                               
"""


@auto_log(__name__)
def display_credits() -> None:
    """
    Displays the credits for the application.
    """
    print("MC-CALCULATOR v0.3.2 created by: 0xIkari")
    print(
        "For more information, visit: https://github.com/nuclear-treestump/mc-calculator"
    )


@auto_log(__name__)
def main() -> None:
    """
    Main function to run the Minecraft Recipe Calculator application.

    This function provides a menu-driven interface for the user to interact with the application.
    It allows users to create new recipes, list all recipes, calculate ingredients for a recipe,
    and exit the application.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        filename="mccalculator.log",
        filemode="a",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    print("Setting up DB. This may take a moment. . .")
    db.setup_database()
    print(MC_CALC_TITLE)
    while True:
        print("\nOptions:")
        print("1. Create a new recipe")
        print("2. List all recipes")
        print("3. Calculate ingredients for a recipe")
        print("4. Credits")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            rl.create_recipe()
        elif choice == "2":
            rl.list_all_recipes()
        elif choice == "3":
            rl.select_and_calculate_recipe()
        elif choice == "4":
            display_credits()
        elif choice == "5":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
