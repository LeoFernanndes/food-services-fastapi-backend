from abc import ABC, abstractmethod
from typing import List

from domain.recipes.entities.recipe_ingredient import RecipeIngredient


class RecipeIngredientRepository(ABC):
    
    @abstractmethod
    def delete(self, id: int) -> None:
        pass
    
    @abstractmethod
    def get_all(self, limit: int = 1000, offset: int = 0) -> List[RecipeIngredient]:
        pass   
    
    @abstractmethod
    def get_by_id(self, id: int) -> RecipeIngredient:
        pass
    
    @abstractmethod
    def save(self, ingredient: RecipeIngredient) -> RecipeIngredient:
        pass
