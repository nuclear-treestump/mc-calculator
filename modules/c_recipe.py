import json
from .c_crafting_block import CraftingBlock as cb

class Recipe:
    def __init__(self, name, crafting_block, shaped=False, slots=None, ingredients=None):
        self.name = name
        self.crafting_block = crafting_block
        self.shaped = shaped
        self.slots = slots if slots else {}
        self.ingredients = ingredients if ingredients else {}

    def to_json(self):

        recipe_dict = self.__dict__.copy()
        recipe_dict['crafting_block'] = self.crafting_block.name
        return json.dumps(recipe_dict)

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)
        crafting_block = cb.get_block(data['crafting_block'])
        return Recipe(name=data['name'], crafting_block=crafting_block, 
                      shaped=data['shaped'], slots=data['slots'], ingredients=data['ingredients'])
