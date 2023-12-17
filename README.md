# Minecraft Recipe Calculator

## Overview
The Minecraft Recipe Calculator is a Python-based tool designed for Minecraft. It tells you how many items you need to make a specific recipe.

## Key Features
- **Recipe Creation**: Users can create custom recipes by specifying the name of the item and the ingredients required, along with their quantities. This now supports nested recipes.
- **Recipe Database**: Recipes are saved in a SQLite database, allowing for easy retrieval and management. This also helps in preventing the creation of duplicate recipes.
- **Ingredient Calculation**: The application can calculate the total amount of each ingredient needed based on the desired quantity of the final crafted item.
- **Recipe Browsing**: Users can view a list of all saved recipes and select one for ingredient calculation.

## How to Use
1. **Run the Application**: Start the application to access the main menu.
2. **Create a New Recipe**: Choose to create a new recipe and follow the prompts to enter the item name, ingredients, and their quantities.
3. **View Recipes**: Select the option to view all available recipes in the database.
4. **Calculate Ingredients**: Choose a recipe and specify the number of final items you wish to craft. The application will display the total ingredients required.

## Installation
To run the Minecraft Recipe Calculator, you will need:
- Python installed on your system.
- SQLite for the database functionality.

Clone the repository to your local machine and run the Python script to start the application.
