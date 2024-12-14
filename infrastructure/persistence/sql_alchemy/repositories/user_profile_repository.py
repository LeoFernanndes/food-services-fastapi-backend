from typing import List

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domain.account_management.entities.user_profile import UserProfile
from domain.account_management.repositories.user_profile_repository import UserProfileRepository
from domain.base.exceptions import DatabaseIntegrityError
from infrastructure.persistence.sql_alchemy.models.UserProfile import UserProfileOrmModel
from infrastructure.persistence.sql_alchemy.repositories.base_sql_alchemy_repository import BaseSqlAlchemyRepository


class UserProfileSqlAlchemyRepository(BaseSqlAlchemyRepository, UserProfileRepository):

    def __init__(self, session: Session):
        BaseSqlAlchemyRepository.__init__(self, session)

    def delete(self, id: int) -> None:
        user_profile: UserProfileOrmModel = self._session.query(UserProfileOrmModel).get({'id': id})
        if not user_profile:
            raise Exception(f'UserProfile with id {id} not found.')
        self._session.delete(user_profile)
        self._session.commit()
        return None

    def get_all(self, limit: int = 1000, offset: int = 0) -> List[UserProfile]:
        user_profiles = self._session.query(UserProfileOrmModel).order_by(UserProfileOrmModel.id).offset(offset).limit(limit).all()
        return [user_profile.to_domain() for user_profile in user_profiles]

    def get_by_id(self, id: int) -> UserProfile | None:
        user_profile: UserProfileOrmModel = self._session.query(UserProfileOrmModel).get({'id': id})
        if not user_profile:
            return None
        return user_profile.to_domain()

    def get_by_user_id(self, id) -> List[UserProfile]:
        user_profiles = self._session.query(UserProfileOrmModel).filter_by(user_id=id)
        return [user_profile.to_domain() for user_profile in user_profiles]

    def save(self, user_profile: UserProfile) -> UserProfile:
        existent_user_profile: UserProfileOrmModel = self._session.query(UserProfileOrmModel).get({'id': user_profile.id})
        if existent_user_profile:
            try:
                existent_user_profile.first_name = user_profile.first_name
                existent_user_profile.last_name = user_profile.last_name
                existent_user_profile.age = user_profile.age
                existent_user_profile.profile_picture = user_profile.profile_picture
                self._session.merge(existent_user_profile)
                self._session.commit()
                return existent_user_profile.to_domain()
            except IntegrityError as e:
                raise DatabaseIntegrityError(f'{e}')
        else:
            try:
                new_user_profile = UserProfileOrmModel.from_entity(user_profile)
                self._session.add(new_user_profile)
                self._session.commit()
                self._session.refresh(new_user_profile)
                return new_user_profile.to_domain()
            except IntegrityError as e:
                raise DatabaseIntegrityError(f'{e}')
