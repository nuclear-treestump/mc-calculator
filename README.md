# Minecraft Recipe Calculator

![GitHub tag (with filter)](https://img.shields.io/github/v/tag/nuclear-treestump/mc-calculator?label=Version)
![PyPI - Version](https://img.shields.io/pypi/v/mc-calculator)
![GitHub all releases](https://img.shields.io/github/downloads/nuclear-treestump/mc-calculator/total)
![GitHub Release Date - Published_At](https://img.shields.io/github/release-date/nuclear-treestump/mc-calculator)


## Overview
The Minecraft Recipe Calculator is a Python-based tool designed for Minecraft. It tells you how many items you need to make a specific recipe.

## Key Features
- **Recipe Creation**: Users can create custom recipes by specifying the name of the item and the ingredients required, along with their quantities. This now supports nested recipes.
- **Recipe Database**: Recipes are saved in a SQLite database, allowing for easy retrieval and management. This also helps in preventing the creation of duplicate recipes.
- **Ingredient Calculation**: The application can calculate the total amount of each ingredient needed based on the desired quantity of the final crafted item.
- **Recipe Browsing**: Users can view a list of all saved recipes and select one for ingredient calculation.

## How to Use
### Pre-Requisites
1. **Make sure you have python installed**: Validate this by running `python --version` in your terminal.
    - If you don't, you can get it here: [Python Release 3.11.7](https://www.python.org/downloads/release/python-3117/). 
    - If it outputs `Python 3.11.7` (or higher), then congratulations, you've installed forbidden snake technology.
2. **Make sure you have pip installed**: Check if you have pip installed by running `pip --version` in your terminal.
    - If you don't have pip, don't worry! You can easily install it by following the instructions on the [pip official website](https://pip.pypa.io/en/stable/installation/)
    - Note: Depending on your system, you might need to use `pip3` instead of `pip`.

### Installation
1. **Install the package**: Install the package via pip by running `pip install mc-calculator`
    - If you've downloaded the `.whl` file from the releases, you can install it by running `pip install /path/to/mc_calculator-0.3.2-py3-none-any.whl`
2. **Confirm the package installed correctly**: Run `mc-calculator` from the terminal. If its installed correctly, you'll get a menu that looks like this:
    ```

          __      __             __                 ___  __   __
    |\/| /    __ /     /\  |    /    |  | |     /\   |  /  \ |__)
    |  | \__     \__  /--\ |___ \__  \__/ |___ /--\  |  \__/ |  \



    Options:
    1. Create a new recipe
    2. List all recipes
    3. Calculate ingredients for a recipe
    4. Credits
    5. Exit
    Choose an option:
    ```
    If you see this, you've installed the project successfully! Good job!

### Usage:
1. **Create a New Recipe**: Choose to create a new recipe and follow the prompts to enter the item name, ingredients, and their quantities.
2. **View Recipes**: Select the option to view all available recipes in the database.
3. **Calculate Ingredients**: Choose a recipe and specify the number of final items you wish to craft. The application will display the total ingredients required.
4. **Credits**: Choose to view the credits.
5. **Close the program**: Choose to close the app.


## Report A Problem:
- Found a bug? Got an idea to make mc-calculator even more useful? [Raise an Issue here!](https://github.com/nuclear-treestump/mc-calculator/issues)
