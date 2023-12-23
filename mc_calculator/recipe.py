"""
This module defines the Recipe class, used for creating and manipulating
crafting recipes in the Minecraft Recipe Calculator application.
"""
import json
from typing import Dict, Optional
from .crafting_block import CraftingBlock


class Recipe:
    """
    Represents a recipe for crafting items in Minecraft.

    Attributes:
        name (str): Name of the recipe.
        crafting_block (CraftingBlock): Crafting block used for the recipe.
        output_count (int): Number of items produced by the recipe.
        shaped (bool): Indicates if the recipe is shaped.
        slots (dict): Slot configuration for the recipe.
        ingredients (dict): Ingredients required for the recipe.
        nested_recipes (dict): Nested recipes within this recipe.
    """

    def __init__(
        self,
        name: str,
        crafting_block: CraftingBlock,
        output_count: int = 1,
        shaped: bool = False,
        slots: Optional[Dict] = None,
        ingredients: Optional[Dict[str, int]] = None,
        nested_recipes: Optional[Dict[int, int]] = None,
    ) -> None:
        self.name = name
        self.crafting_block = (
            crafting_block
            if isinstance(crafting_block, CraftingBlock)
            else CraftingBlock.get_block(crafting_block)
        )
        self.output_count = output_count
        self.shaped = shaped
        self.slots = slots if slots else {}
        self.ingredients = ingredients if ingredients else {}
        self.nested_recipes = (
            nested_recipes if nested_recipes else {}
        )  # Format: {recipe_id: quantity, ...}

    def to_json(self) -> str:
        """
        Converts the recipe into a JSON string.

        Returns:
            str: JSON string representation of the recipe.
        """
        recipe_dict = self.__dict__.copy()
        recipe_dict["crafting_block"] = self.crafting_block.name
        return json.dumps(recipe_dict)

    @staticmethod
    def from_json(
        json_str: str, nested_recipes_json_str: Optional[str] = None
    ) -> "Recipe":
        """
        Creates a Recipe object from JSON strings.

        Args:
            json_str (str): JSON string representing the basic recipe.
            nested_recipes_json_str (str, optional): JSON string representing nested recipes.

        Returns:
            Recipe: A Recipe object created from the JSON strings.
        """
        data = json.loads(json_str)
        crafting_block = CraftingBlock.get_block(data["crafting_block"])

        nested_recipes = {}
        if nested_recipes_json_str is not None:
            nested_recipes = json.loads(nested_recipes_json_str)
        else:
            nested_recipes = data.get(
                "nested_recipes", {}
            )  # for backward compatibility

        return Recipe(
            name=data["name"],
            crafting_block=crafting_block,
            output_count=data["output_count"],
            shaped=data["shaped"],
            slots=data["slots"],
            ingredients=data["ingredients"],
            nested_recipes=nested_recipes,
        )
