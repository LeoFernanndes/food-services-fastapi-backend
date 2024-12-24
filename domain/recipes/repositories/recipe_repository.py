from abc import ABC, abstractmethod
from typing import List

from domain.recipes.entities.recipe import Recipe


class RecipeRepository(ABC):
    
    @abstractmethod
    def delete(self, id: int) -> None:
        pass
    
    @abstractmethod
    def get_all(self, limit: int = 1000, offset: int = 0) -> List[Recipe]:
        pass
    
    @abstractmethod
    def get_by_id(self, id: int) -> Recipe:
        pass
    
    @abstractmethod
    def save(self, recipe: Recipe) -> Recipe:
        pass
