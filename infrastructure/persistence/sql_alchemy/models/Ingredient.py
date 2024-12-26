from typing import Self

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.recipes.entities.ingredient import Ingredient
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel
from infrastructure.persistence.sql_alchemy.models.Recipes import RecipeOrmModel


class IngredientOrmModel(Base, BaseOrmModel):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=False)
    ingredient_measurement_unit_id = mapped_column(ForeignKey('ingredient_measurement_units.id'))
    ingredient_measurement_unit: Mapped['IngredientMeasurementUnitOrmModel'] = relationship(back_populates='ingredient')
    recipe_id = mapped_column(ForeignKey('recipes.id'))
    recipe: Mapped['RecipeOrmModel'] = relationship(back_populates='ingredients')

    def to_domain(self) -> Ingredient:
        return Ingredient(id=self.id, name=self.name, ingredient_measurement_unit_id=self.ingredient_measurement_unit_id, recipe_id=self.recipe_id)

    @classmethod
    def from_entity(cls, entity: Ingredient) -> Self:
        return IngredientOrmModel(id=entity.id, name=entity.name, ingredient_measurement_unit_id=entity.ingredient_measurement_unit_id, recipe_id=entity.recipe_id)
