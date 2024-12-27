from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.base import exceptions as domain_exceptions
from domain.recipes.entities.recipe_ingredient import RecipeIngredient
from domain.recipes.repositories.recipe_ingredient_repository import RecipeIngredientRepository
from infrastructure.persistence.sql_alchemy.models.RecipeIngredient import RecipeIngredientOrmModel
from infrastructure.persistence.sql_alchemy.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository


class RecipeIngredientSqlAlchemyRepository(BaseSqlAlchemyRepository, RecipeIngredientRepository):

    def __init__(self, session: Session):
        BaseSqlAlchemyRepository.__init__(self, session)

    def delete(self, id: int) -> None:
        ingredient_orm = self._session.query(RecipeIngredientOrmModel).filter(RecipeIngredientOrmModel.id == id).first()
        self._session.delete(ingredient_orm)
        self._session.commit()
        return None

    def get_all(self, limit: int = 1000, offset: int = 0) -> List[RecipeIngredient]:
        ingredients_orm = self._session.query(RecipeIngredientOrmModel).order_by(RecipeIngredientOrmModel.id).offset(offset).limit(limit).all()
        if not ingredients_orm:
            return []
        return [i.to_domain() for i in ingredients_orm]

    def get_by_id(self, id: int) -> RecipeIngredient:
        ingredient_orm = self._session.query(RecipeIngredientOrmModel).filter(RecipeIngredientOrmModel.id == id).first()
        if not ingredient_orm:
            raise domain_exceptions.NotFoundDomainException()
        return ingredient_orm.to_domain()

    def save(self, ingredient: RecipeIngredient) -> RecipeIngredient:
        persisted_object: RecipeIngredientOrmModel = self._session.query(RecipeIngredientOrmModel).filter(RecipeIngredientOrmModel.id == ingredient.id).first()
        if persisted_object:
            try:
                persisted_object.quantity = ingredient.quantity
                persisted_object.ingredient_measurement_unit_id = ingredient.ingredient_measurement_unit_id
                self._session.merge(persisted_object)
                self._session.commit()
                return persisted_object.to_domain()
            except IntegrityError as e:
                raise domain_exceptions.DatabaseIntegrityDomainException()
            except Exception as e:
                pass
        else:
            try:
                orm_object = RecipeIngredientOrmModel.from_entity(ingredient)
                self._session.add(orm_object)
                self._session.commit()
                self._session.refresh(orm_object)
                return orm_object.to_domain()
            except IntegrityError as e:
                raise domain_exceptions.DatabaseIntegrityDomainException()
            except Exception as e:
                pass
