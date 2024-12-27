from abc import ABC, abstractmethod
from typing import List

from domain.recipes.entities.recipe_ingredient import RecipeIngredient


class RecipeIngredientRepository(ABC):
    
    @abstractmethod
    def delete(self, recipe_id: int, id: int) -> None:
        pass
    
    @abstractmethod
    def get_all(self, recipe_id: int, limit: int = 1000, offset: int = 0) -> List[RecipeIngredient]:
        pass   
    
    @abstractmethod
    def get_by_id(self, recipe_id: int, id: int) -> RecipeIngredient:
        pass
    
    @abstractmethod
    def save(self, recipe_id: int, ingredient: RecipeIngredient) -> RecipeIngredient:
        pass
