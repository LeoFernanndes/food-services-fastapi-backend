from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.base.exceptions import DatabaseIntegrityError
from domain.recipes.entities.ingredient_measurement_unit import IngredientMeasurementUnit
from domain.recipes.repositories.ingredient_measurement_unit_repository import IngredientMeasurementUnitRepository
from infrastructure.persistence.sql_alchemy.models.IngredientMeasurementUnit import IngredientMeasurementUnitOrmModel
from infrastructure.persistence.sql_alchemy.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository


class IngredientMeasurementUnitRepository(BaseSqlAlchemyRepository, IngredientMeasurementUnitRepository):

    def __init__(self, session: Session):
        BaseSqlAlchemyRepository.__init__(self, session)

    def delete(self, id: int) -> None:
        unit = self._session.query(IngredientMeasurementUnitOrmModel).filter(IngredientMeasurementUnitOrmModel.id == id).first()
        if not unit:
            raise DatabaseIntegrityError("User not found.")
        self._session.delete(unit)
        self._session.commit()
        return None

    def get_all(self, limit: int = 1000, offset: int = 0) -> List[IngredientMeasurementUnit]:
        units = self._session.query(IngredientMeasurementUnitOrmModel).order_by(IngredientMeasurementUnitOrmModel.id).offset(offset).limit(limit).all()
        if not units:
            return []
        return [unit.to_domain() for unit in units]

    def get_by_id(self, id: int) -> IngredientMeasurementUnit:
        unit = self._session.query(IngredientMeasurementUnitOrmModel).filter(IngredientMeasurementUnitOrmModel.id == id).first()
        if not unit:
            return None
        return unit.to_domain()

    def save(self, ingredient_measurement_unit: IngredientMeasurementUnit) -> IngredientMeasurementUnit:
        persisted_object = self._session.query(IngredientMeasurementUnitOrmModel).filter(IngredientMeasurementUnitOrmModel.id == ingredient_measurement_unit.id).first()
        if persisted_object:
            try:
                persisted_object.name = ingredient_measurement_unit.name
                self._session.merge(persisted_object)
                self._session.commit()
                return persisted_object.to_domain()
            except IntegrityError as e:
                raise DatabaseIntegrityError("Database integrity error.")
        else:
            try:
                orm_object = IngredientMeasurementUnitOrmModel.from_entity(ingredient_measurement_unit)
                self._session.add(orm_object)
                self._session.commit()
                self._session.refresh(orm_object)
                return orm_object.to_domain()
            except IntegrityError as e:
                raise DatabaseIntegrityError("Database integrity error.")
