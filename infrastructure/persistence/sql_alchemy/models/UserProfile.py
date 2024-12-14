from typing import Self

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domain.account_management.entities.user_profile import UserProfile
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel


class UserProfileOrmModel(Base, BaseOrmModel):
    __tablename__ = "user_profiles"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name = mapped_column(String, nullable=False, unique=False)
    last_name = mapped_column(String, nullable=False, unique=False)
    age = mapped_column(Integer, nullable=False)
    profile_picture = mapped_column(String, nullable=True, unique=False)
    user_id = mapped_column(ForeignKey('users.id'))

    def to_domain(self) -> UserProfile:
        return UserProfile(self.id, self.first_name, self.last_name, self.age, self.profile_picture, self.user_id)

    @classmethod
    def from_entity(cls, user_profile: UserProfile) -> Self:
        user_profile_orm = UserProfileOrmModel()
        user_profile_orm.id = user_profile.id
        user_profile_orm.first_name = user_profile.first_name
        user_profile_orm.last_name = user_profile.last_name
        user_profile_orm.age = user_profile.age
        user_profile_orm.profile_picture = user_profile.profile_picture
        user_profile_orm.user_id = user_profile.user_id
        return user_profile_orm
