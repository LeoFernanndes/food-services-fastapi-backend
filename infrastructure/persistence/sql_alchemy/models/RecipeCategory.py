from typing import Self

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from domain.recipes.entities.recipe_category import RecipeCategory
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel


class RecipeCategoryOrmModel(Base, BaseOrmModel):
    __tablename__ = "recipe_categories"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, unique=True)

    def to_domain(self) -> RecipeCategory:
        return RecipeCategory(id=self.id, name=self.name)

    @classmethod
    def from_entity(cls, entity: RecipeCategory) -> Self:
        return RecipeCategoryOrmModel(id=entity.id, name=entity.name)
