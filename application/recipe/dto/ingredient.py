from pydantic import BaseModel

from application.base import base_dto


class BaseIngredientDto(BaseModel):
    pass


class IngredientCreateDto(BaseIngredientDto):
    name: str


class IngredientDto(IngredientCreateDto):
    id: int


class IngredientUpdateDto(IngredientCreateDto):
    name: str
