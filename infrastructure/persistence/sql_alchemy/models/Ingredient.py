from typing import Self

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.recipes.entities.ingredient import Ingredient
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel


class IngredientOrmModel(Base, BaseOrmModel):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)

    def to_domain(self) -> Ingredient:
        return Ingredient(id=self.id, name=self.name)

    @classmethod
    def from_entity(cls, entity: Ingredient) -> Self:
        return IngredientOrmModel(id=entity.id, name=entity.name)
