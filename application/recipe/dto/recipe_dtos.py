from typing import List

from application.base.base_dto import BaseDto
from application.recipe.dto.ingredient_dtos import IngredientCreateDto


class BaseRecipeDto(BaseDto):
    pass


class RecipeCreateDto(BaseRecipeDto):
    name: str
    title: str
    description: str
    user_profile_id: int
    preparation_time_minutes: int
    preparation_steps: str
    main_image: str
    portions_quantity: int
    category_id: int


class RecipeDto(RecipeCreateDto):
    id: int


class RecipeUpdateDto(BaseRecipeDto):
    name: str
    title: str
    description: str
    preparation_time_minutes: int
    preparation_steps: str
    main_image: str
    portions_quantity: int
    category_id: int
