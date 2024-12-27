from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.base import exceptions as domain_exceptions
from domain.recipes.entities.ingredient import Ingredient
from domain.recipes.repositories.ingredient_repository import IngredientRepository
from infrastructure.persistence.sql_alchemy.models.Ingredient import IngredientOrmModel
from infrastructure.persistence.sql_alchemy.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository


class IngredientSqlAlchemyRepository(BaseSqlAlchemyRepository, IngredientRepository):

    def __init__(self, session: Session):
        BaseSqlAlchemyRepository.__init__(self, session)

    def delete(self, id: int) -> None:
        unit = self._session.query(IngredientOrmModel).filter(IngredientOrmModel.id == id).first()
        if not unit:
            raise domain_exceptions.NotFoundDomainException()
        try:
            self._session.delete(unit)
            self._session.commit()
        except IntegrityError as e:
            raise domain_exceptions.DatabaseIntegrityDomainException()
        return None

    def get_all(self, limit: int = 1000, offset: int = 0) -> List[Ingredient]:
        orm_objects = self._session.query(IngredientOrmModel).order_by(IngredientOrmModel.id).offset(offset).limit(limit).all()
        if not orm_objects:
            return []
        return [orm_object.to_domain() for orm_object in orm_objects]

    def get_by_id(self, id: int) -> Ingredient:
        unit = self._session.query(IngredientOrmModel).filter(IngredientOrmModel.id == id).first()
        if not unit:
            raise domain_exceptions.NotFoundDomainException()
        return unit.to_domain()

    def save(self, ingredient: Ingredient) -> Ingredient:
        persisted_object = self._session.query(IngredientOrmModel).filter(IngredientOrmModel.id == ingredient.id).first()
        if persisted_object:
            try:
                persisted_object.name = ingredient.name
                self._session.merge(persisted_object)
                self._session.commit()
                return persisted_object.to_domain()
            except IntegrityError as e:
                raise domain_exceptions.DatabaseIntegrityDomainException()
        else:
            try:
                orm_object = IngredientOrmModel.from_entity(ingredient)
                self._session.add(orm_object)
                self._session.commit()
                self._session.refresh(orm_object)
                return orm_object.to_domain()
            except IntegrityError as e:
                raise domain_exceptions.DatabaseIntegrityDomainException()
