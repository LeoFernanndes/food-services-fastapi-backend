from abc import ABC, abstractmethod
from typing import List

from domain.recipes.entities.recipe_category import RecipeCategory


class RecipeCategoryRepository(ABC):
    
    @abstractmethod
    def delete(self, id: int) -> None:
        pass

    @abstractmethod
    def get_all(self, limit: int = 1000, offset: int = 0) -> List[RecipeCategory]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> RecipeCategory:
        pass
    
    @abstractmethod
    def save(self, category: RecipeCategory) -> RecipeCategory:
        pass
