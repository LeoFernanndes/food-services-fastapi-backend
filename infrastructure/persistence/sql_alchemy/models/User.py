from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

from domain.authentication.entities.user import User
from infrastructure.persistence.sql_alchemy.database import Base
from infrastructure.persistence.sql_alchemy.models.Base import BaseOrmModel


class UserOrmModel(Base, BaseOrmModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    def to_domain(self) -> User:
        return User(self.id, self.username, self.email, self.password)

    @staticmethod
    def from_entity(user: User):
        return UserOrmModel(id=user.id, username=user.username, email=user.email, password=user.password)
