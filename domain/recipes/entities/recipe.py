from typing import List, Self

from domain.base.base_entity import BaseEntity
from domain.account_management.entities.user_profile import UserProfile
from domain.recipes.entities.recipe_category import RecipeCategory
from domain.recipes.entities.ingredient import Ingredient


class Recipe(BaseEntity):
    def __init__(self, id: int | None, name: str, title: str, description: str,
        user_profile_id: int, preparation_time_minutes: int,
        preparation_steps: str, main_image: str, portions_quantity: int,
        category_id: id
    ):
        self.id = id
        self.name = name
        self.title = title
        self.description = description
        self.user_profile_id = user_profile_id
        self.preparation_time_minutes = preparation_time_minutes
        self.preparation_steps = preparation_steps
        self.main_image = main_image
        self.portions_quantity = portions_quantity
        self.category_id = category_id
