from typing import List, Self

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from domain.recipes.entities.recipe import Recipe
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel


class RecipeOrmModel(Base, BaseOrmModel):
    __tablename__ = "recipes"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    name = mapped_column(String, nullable=False, unique=False)
    title = mapped_column(String, nullable=False, unique=False)
    description = mapped_column(String, nullable=False, unique=False)
    user_profile_id = mapped_column(ForeignKey('user_profiles.id'))
    preparation_steps = mapped_column(String, nullable=False, unique=False)
    main_image = mapped_column(String, nullable=False, unique=False)
    portions_quantity = mapped_column(Integer, nullable=False, unique=False)
    category_id = mapped_column(ForeignKey('ingredient_categories.id'))
    ingredients = Mapped[List["IngredientOrmModel"]] = relationship()
