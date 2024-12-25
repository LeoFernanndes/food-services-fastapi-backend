from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.base.exceptions import DatabaseIntegrityError, NotFoundDomainException
from domain.recipes.entities.recipe_category import RecipeCategory
from domain.recipes.repositories.recipe_category_repository import RecipeCategoryRepository
from infrastructure.persistence.sql_alchemy.models.RecipeCategory import RecipeCategoryOrmModel
from infrastructure.persistence.sql_alchemy.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository


class RecipeCategorySqlAlchemyRepository(BaseSqlAlchemyRepository, RecipeCategoryRepository):

    def __init__(self, session: Session):
        BaseSqlAlchemyRepository.__init__(self, session)

    def delete(self, id: int) -> None:
        orm_entity = self._session.query(RecipeCategoryOrmModel).filter(RecipeCategoryOrmModel.id == id).first()
        if not orm_entity:
            raise NotFoundDomainException('Not found.')
        self._session.delete(orm_entity)
        self._session.commit()
        return None

    def get_all(self, limit: int = 1000, offset: int = 0) -> List[RecipeCategory]:
        categories_orm = self._session.query(RecipeCategoryOrmModel).order_by(RecipeCategoryOrmModel.id).offset(offset).limit(limit).all()
        if not categories_orm:
            return []
        return [c.to_domain() for c in categories_orm]

    def get_by_id(self, id: int) -> RecipeCategory:
        category_orm = self._session.query(RecipeCategoryOrmModel).filter(RecipeCategoryOrmModel.id == id).first()
        if not category_orm:
            raise NotFoundDomainException('Not found.')
        return category_orm.to_domain()

    def save(self, category: RecipeCategory) -> RecipeCategory:
        persisted_object = self._session.query(RecipeCategoryOrmModel).filter(RecipeCategoryOrmModel.id == category.id).first()
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
                orm_object = RecipeCategoryOrmModel.from_entity(category)
                self._session.add(orm_object)
                self._session.commit()
                self._session.refresh(orm_object)
                return orm_object.to_domain()
            except IntegrityError as e:
                raise DatabaseIntegrityError("Database integrity error.")
