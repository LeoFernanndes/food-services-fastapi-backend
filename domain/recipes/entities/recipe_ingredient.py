from typing import Self 

from domain.base.base_entity import BaseEntity
from domain.recipes.entities.ingredient_measurement_unit import IngredientMeasurementUnit


class RecipeIngredient(BaseEntity):
    def __init__(
        self, id: int | None,
        quantity: int,
        ingredient_id: int,
        ingredient_measurement_unit_id: int,
        recipe_id: int
    ):
        self.id = id
        self.quantity = quantity
        self.ingredient_id = ingredient_id
        self.ingredient_measurement_unit_id = ingredient_measurement_unit_id
        self.recipe_id = recipe_id
