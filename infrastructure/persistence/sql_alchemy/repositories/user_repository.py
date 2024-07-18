from typing import List

from domain.authentication.entities.user import User
from domain.authentication.repositories.user_repository import UserRepository
from infrastructure.persistence.sql_alchemy.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository
from infrastructure.persistence.sql_alchemy.models.User import UserOrmModel


class UserSqlAlchemyRepository(BaseSqlAlchemyRepository, UserRepository):

    def __init__(self, db_session):
        BaseSqlAlchemyRepository.__init__(self, db_session)

    def get_by_id(self, id: int) -> User | None:
        user: UserOrmModel = self._session.query(UserOrmModel).filter(UserOrmModel.id == id).first()
        if not user:
            return None
        return user.to_domain()

    def get_all(self, limit: int = 1000, offset: int = 0) -> List[User]:
        users = self._session.query(UserOrmModel).order_by(UserOrmModel.id).offset(offset).limit(limit).all()
        if not users:
            return []
        return [user.to_domain() for user in users]

    def save(self, user: User) -> User:
        old_user = self._session.query(UserOrmModel).filter(UserOrmModel.id == user.id).first()
        if old_user:
            old_user.email = user.email
            old_user.username = user.username
            old_user.password = user.password
            self._session.merge(old_user)
            self._session.commit()
            return old_user

        user_orm_model = UserOrmModel.from_entity(user)
        self._session.add(user_orm_model)
        self._session.commit()
        self._session.refresh(user_orm_model)
        return user_orm_model.to_domain()

    def delete(self, id: int) -> None:
        pass
