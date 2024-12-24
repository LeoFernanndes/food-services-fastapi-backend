from typing import Self

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.recipes.entities.ingredient import Ingredient
from domain.recipes.entities.ingredient_measurement_unit import IngredientMeasurementUnit
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel


class IngredientOrmModel(Base, BaseOrmModel):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, auto_increment=True)
    name = Column(String, nullable=False, unique=False)
    ingredient_measurement_unit_id = mapped_column(ForeignKey('ingredient_measurement_units.id'))
    ingredient_measurement_unit: Mapped['IngredientMeasurementUnit'] = relationship(back_populates='ingredient_measurement_units')
    recipe_id = mapped_column(ForeignKey('recipes.id'))

    def to_domain(self) -> Ingredient:
        return Ingredient(id=self.id, name=self.name, ingredient_measurement_unit=self.ingredient_measurement_unit)

    @classmethod
    def from_entity(cls, entity: Ingredient) -> Self:
        return IngredientOrmModel(id=entity.id, name=entity.name, ingredient_measurement_unit_id=entity.ingredient_measurement_unit.id)
