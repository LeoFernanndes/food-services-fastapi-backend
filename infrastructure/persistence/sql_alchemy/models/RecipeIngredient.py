from typing import Self

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.recipes.entities.recipe_ingredient import RecipeIngredient
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel
from infrastructure.persistence.sql_alchemy.models.Recipes import RecipeOrmModel


class RecipeIngredientOrmModel(Base, BaseOrmModel):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer, nullable=False)
    ingredient_id = mapped_column(ForeignKey('ingredients.id'))
    ingredient: Mapped['IngredientOrmModel'] = relationship()
    ingredient_measurement_unit_id = mapped_column(ForeignKey('ingredient_measurement_units.id'))
    ingredient_measurement_unit: Mapped['IngredientMeasurementUnitOrmModel'] = relationship(back_populates='recipe_ingredient')
    recipe_id = mapped_column(ForeignKey('recipes.id'))
    recipe: Mapped['RecipeOrmModel'] = relationship(back_populates='recipe_ingredients')

    def to_domain(self) -> RecipeIngredient:
        return RecipeIngredient(id=self.id, quantity=self.quantity, ingredient_id=self.ingredient_id, ingredient_measurement_unit_id=self.ingredient_measurement_unit_id, recipe_id=self.recipe_id)

    @classmethod
    def from_entity(cls, entity: RecipeIngredient) -> Self:
        return RecipeIngredientOrmModel(id=entity.id, quantity=entity.quantity, ingredient_id=entity.ingredient_id, ingredient_measurement_unit_id=entity.ingredient_measurement_unit_id, recipe_id=entity.recipe_id)
