from typing import Self

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.recipes.entities.ingredient_measurement_unit import IngredientMeasurementUnit
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel


class IngredientMeasurementUnitOrmModel(Base, BaseOrmModel):

    __tablename__ = "ingredient_measurement_units"
    
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, unique=True)
    ingredient: Mapped['IngredientOrmModel'] = relationship(back_populates='ingredient_measurement_unit')

    def to_domain(self) -> IngredientMeasurementUnit:
        return IngredientMeasurementUnit(id=self.id, name=self.name)

    @classmethod
    def from_entity(cls, entity: IngredientMeasurementUnit) -> Self:
        return IngredientMeasurementUnitOrmModel(id=entity.id, name=entity.name)
