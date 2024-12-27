from abc import ABC, abstractmethod
from typing import List

from domain.recipes.entities.ingredient import Ingredient


class IngredientRepository(ABC):

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

    @abstractmethod
    def get_all(self, limit: int = 1000, offset: int = 0) -> List[Ingredient]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Ingredient:
        pass

    @abstractmethod
    def save(self, ingredient_measurement_unit: Ingredient) -> Ingredient:
        pass
