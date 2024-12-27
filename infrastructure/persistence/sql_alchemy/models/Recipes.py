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
    user_profile: Mapped["UserProfileOrmModel"] = relationship()
    preparation_time_minutes = mapped_column(Integer, nullable=False)
    preparation_steps = mapped_column(String, nullable=False, unique=False)
    main_image = mapped_column(String, nullable=False, unique=False)
    portions_quantity = mapped_column(Integer, nullable=False, unique=False)
    category_id = mapped_column(ForeignKey('recipe_categories.id'))
    category: Mapped["CategoryOrmModel"] = relationship("RecipeCategoryOrmModel")
    recipe_ingredients: Mapped[List["RecipeIngredientOrmModel"]] = relationship("RecipeIngredientOrmModel")

    def to_domain(self) -> Recipe:
        # ingredients_entities = [i.to_domain() for i in self.ingredients]
        # user_profile_entity = self.user_profile.to_domain()
        # category_entity = self.category.to_domain()
        return Recipe(
            id=self.id, name=self.name, title=self.title, description=self.description,
            user_profile_id=self.user_profile_id, preparation_time_minutes=self.preparation_time_minutes,
            preparation_steps=self.preparation_steps, main_image=self.main_image,
            portions_quantity=self.portions_quantity, category_id=self.category_id
        )

    @classmethod
    def from_entity(cls, entity: Recipe) -> Self:
        return RecipeOrmModel(
            id=entity.id, name=entity.name, title=entity.title,
            description=entity.description, user_profile_id=entity.user_profile_id,
            preparation_time_minutes=entity.preparation_time_minutes,
            preparation_steps=entity.preparation_steps, main_image=entity.main_image,
            portions_quantity=entity.portions_quantity, category_id=entity.category_id
        )
