from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.base import exceptions as domain_exceptions
from domain.recipes.entities.recipe import Recipe
from domain.recipes.repositories.recipe_repository import RecipeRepository
from infrastructure.persistence.sql_alchemy.models.Recipes import RecipeOrmModel
from infrastructure.persistence.sql_alchemy.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository


class RecipeSqlAlchemyRepository(BaseSqlAlchemyRepository, RecipeRepository):
    def __init__(self, session: Session):
        BaseSqlAlchemyRepository.__init__(self, session)

    def delete(self, id: int) -> None:
        recipe_orm = self._session.query(RecipeOrmModel).filter(RecipeOrmModel.id == id).first()
        self._session.delete(recipe_orm)
        self._session.commit()
        return None

    def get_all(self, limit: int = 1000, offset: int = 0) -> List[Recipe]:
        recipes_orm = self._session.query(RecipeOrmModel).order_by(RecipeOrmModel.id).offset(offset).limit(limit).all()
        if not recipes_orm:
            return []
        return [r.to_domain() for r in recipes_orm]

    def get_by_id(self, id: int) -> Recipe:
        recipe_orm = self._session.query(RecipeOrmModel).filter(RecipeOrmModel.id == id).first()
        if not recipe_orm:
            raise domain_exceptions.NotFoundDomainException
        return recipe_orm.to_domain()

    def save(self, recipe: Recipe) -> Recipe:
        orm_object = self._session.query(RecipeOrmModel).filter(RecipeOrmModel.id == recipe.id).first()
        if orm_object:
            try:
                orm_object.name = recipe.name
                orm_object.title = recipe.title
                orm_object.description = recipe.description
                orm_object.preparation_time_minutes = recipe.preparation_time_minutes
                orm_object.preparation_steps = recipe.preparation_steps
                orm_object.main_image = recipe.main_image
                orm_object.portions_quantity = recipe.portions_quantity
                orm_object.category_id = recipe.category_id
                self._session.merge(orm_object)
                self._session.commit()
                return orm_object.to_domain()
            except IntegrityError as e:
                raise domain_exceptions.DatabaseIntegrityDomainException()
        else:
            try:
                orm_object = RecipeOrmModel.from_entity(recipe)
                self._session.add(orm_object)
                self._session.commit()
                self._session.refresh(orm_object)
                return orm_object.to_domain()
            except IntegrityError as e:
                raise domain_exceptions.DatabaseIntegrityDomainException()
