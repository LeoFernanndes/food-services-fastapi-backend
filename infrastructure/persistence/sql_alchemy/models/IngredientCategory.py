from typing import Self

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from domain.recipes.entities.ingredientcategory import IngredientCategory
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel


class IngredientCategoryOrmModel(Base, BaseOrmModel):
    __tablename__ = "ingredient_categories"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, unique=False)

    def to_domain(self) -> IngredientCategory:
        return IngredientCategory(id=self.id, name=self.name)

    @classmethod
    def from_entity(cls, entity: IngredientCategory) -> Self:
        return IngredientCategoryOrmModel(id=entity.id, name=entity.name)
