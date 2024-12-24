from abc import ABC, abstractmethod
from typing import List

from domain.recipes.entities.ingredientcategory import IngredientCategory


class CategoryRepository(ABC):
    
    @abstractmethod
    def delete(self, id: int) -> None:
        pass

    @abstractmethod
    def get_all(self, limit: int = 1000, offset: int = 0) -> List[IngredientCategory]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> IngredientCategory:
        pass
    
    @abstractmethod
    def save(self, category: IngredientCategory) -> IngredientCategory:
        pass
