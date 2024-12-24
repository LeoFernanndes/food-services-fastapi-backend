from typing import List, Self

from domain.base.base_entity import BaseEntity
from domain.account_management.entities.user_profile import UserProfile
from domain.recipes.entities.ingredientcategory import IngredientCategory
from domain.recipes.entities.ingredient import Ingredient


class Recipe(BaseEntity):
    def __init__(self, id: int | None, name: str, title: str, description: str,
                 user_profile: UserProfile, preparation_time_minutes: int,
                 preparation_steps: str, main_image: str, portions_quantity: int,
                 category: IngredientCategory, ingredients: List[Ingredient]) -> Self:
        self.id = id
        self.name = name
        self.title = title
        self.description = description
        self.user_profile = user_profile
        self.preparation_steps = preparation_steps
        self.main_image = main_image
        self.portions_quantity = portions_quantity
        self.category = category
        self.ingredients = ingredients
