from typing import List

from domain.base.base_entity import BaseEntity


class IngredientMeasurementUnit(BaseEntity):
    def __init__(self, id: int | None, name: str):
        self.id = id
        self.name = name
