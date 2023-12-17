from . import database_ops as db
from . import recipe_logic as rl


def main():
    """
    Main function to run the Minecraft Recipe Calculator application.

    This function provides a menu-driven interface for the user to interact with the application.
    It allows users to create new recipes, list all recipes, calculate ingredients for a recipe,
    and exit the application.
    """
    while True:
        print("\nOptions:")
        print("1. Create a new recipe")
        print("2. List all recipes")
        print("3. Calculate ingredients for a recipe")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            rl.create_recipe()
        elif choice == "2":
            rl.list_all_recipes()
        elif choice == "3":
            rl.select_and_calculate_recipe()
        elif choice == "4":
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    db.setup_database()
    main()
