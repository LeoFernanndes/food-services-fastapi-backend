from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.base.exceptions import DatabaseIntegrityError, NotFoundDomainException
from domain.recipes.entities.ingredientcategory import IngredientCategory
from domain.recipes.repositories.category_repository import CategoryRepository
from infrastructure.persistence.sql_alchemy.models.IngredientCategory import IngredientCategoryOrmModel
from infrastructure.persistence.sql_alchemy.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository


class IngredientCategorySqlAlchemyRepository(BaseSqlAlchemyRepository, CategoryRepository):

    def __init__(self, session: Session):
        BaseSqlAlchemyRepository.__init__(self, session)

    def delete(self, id: int) -> None:
        orm_entity = self._session.query(IngredientCategoryOrmModel).filter(IngredientCategoryOrmModel.id == id).first()
        if not orm_entity:
            raise NotFoundDomainException('Not found.')
        self._session.delete(orm_entity)
        self._session.commit()
        return None

    def get_all(self, limit: int = 1000, offset: int = 0) -> List[IngredientCategory]:
        categories_orm = self._session.query(IngredientCategoryOrmModel).order_by(IngredientCategoryOrmModel.id).offset(offset).limit(limit).all()
        if not categories_orm:
            return []
        return [c.to_domain() for c in categories_orm]

    def get_by_id(self, id: int) -> IngredientCategory:
        category_orm = self._session.query(IngredientCategoryOrmModel).filter(IngredientCategoryOrmModel.id == id).first()
        if not category_orm:
            raise NotFoundDomainException('Not found.')
        return category_orm.to_domain()

    def save(self, category: IngredientCategory) -> IngredientCategory:
        persisted_object = self._session.query(IngredientCategoryOrmModel).filter(IngredientCategoryOrmModel.id == category.id).first()
        if persisted_object:
            try:
                persisted_object.name = category.name
                self._session.merge(persisted_object)
                self._session.commit()
                return persisted_object.to_domain()
            except IntegrityError as e:
                raise DatabaseIntegrityError("Database integrity error.")
        else:
            try:
                orm_object = IngredientCategoryOrmModel.from_entity(category)
                self._session.add(orm_object)
                self._session.commit()
                self._session.refresh(orm_object)
                return orm_object.to_domain()
            except IntegrityError as e:
                raise DatabaseIntegrityError("Database integrity error.")
