from abc import ABC, abstractmethod
from typing import List

from domain.recipes.entities.ingredient_measurement_unit import IngredientMeasurementUnit


class IngredientMeasurementUnitRepository(ABC):
    
    @abstractmethod
    def delete(self, id: int) -> None:
        pass
    
    @abstractmethod
    def get_all(self, limit: int = 1000, offset: int = 0) -> List[IngredientMeasurementUnit]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> IngredientMeasurementUnit:
        pass
    
    @abstractmethod
    def save(self, ingredient_measurement_unit: IngredientMeasurementUnit) -> IngredientMeasurementUnit:
        pass
