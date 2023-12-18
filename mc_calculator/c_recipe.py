import json
from mc_calculator.c_crafting_block import CraftingBlock


class Recipe:
    def __init__(
        self,
        name,
        crafting_block,
        output_count=1,
        shaped=False,
        slots=None,
        ingredients=None,
        nested_recipes=None,
    ):
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

    def to_json(self):
        recipe_dict = self.__dict__.copy()
        recipe_dict["crafting_block"] = self.crafting_block.name
        return json.dumps(recipe_dict)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        crafting_block = CraftingBlock.get_block(data["crafting_block"])
        nested_recipes = data.get("nested_recipes", {})
        return Recipe(
            name=data["name"],
            crafting_block=crafting_block,
            output_count=data["output_count"],
            shaped=data["shaped"],
            slots=data["slots"],
            ingredients=data["ingredients"],
            nested_recipes=nested_recipes,
        )
