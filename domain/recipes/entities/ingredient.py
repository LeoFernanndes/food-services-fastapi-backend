from typing import Self 

from domain.base.base_entity import BaseEntity
from domain.recipes.entities.ingredient_measurement_unit import IngredientMeasurementUnit


class Ingredient(BaseEntity):
    def __init__(
        self, id: int | None,
        name: str, 
        ingredient_measurement_unit_id: int,
        recipe_id: int
    ):
        self.id = id
        self.name = name
        self.ingredient_measurement_unit_id = ingredient_measurement_unit_id
        self.recipe_id = recipe_id
