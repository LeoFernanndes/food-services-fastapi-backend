import os

from dotenv import load_dotenv
from passlib.context import CryptContext
from typing import List

from application.authentication.dtos.user_dtos import UserCreateDto, UserDto, UserUpdateDto
from domain.authentication.entities.user import User
from domain.authentication.repositories.user_repository import UserRepository


load_dotenv()


class UserService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    SECRET_KEY = os.getenv("PASSWORD_HASHING_SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(self, user_create_dto: UserCreateDto) -> UserDto:
        user = User(id=None, username=user_create_dto.username, email=user_create_dto.email, password=self.get_password_hash(user_create_dto.password))
        new_user = self._user_repository.save(user)
        return UserDto(id=new_user.id, username=new_user.username, email=new_user.email, password=new_user.password)

    def get_user_by_id(self, id: int) -> UserDto | None:
        user = self._user_repository.get_by_id(id)
        if not user:
            return None
        return UserDto(id=user.id, username=user.username, email=user.email, password=user.password)
    
    def get_user_by_username(self, username: str) -> UserDto | None:
        user = self._user_repository.get_by_username(username)
        if not user:
            return None
        return UserDto(id=user.id, username=user.username, email=user.email)

    def get_all_users(self, items_per_page: int = 1000, page: int = 0) -> List[UserDto]:
        limit = items_per_page
        offset = items_per_page * page
        users = self._user_repository.get_all(limit, offset)
        return [UserDto(id=u.id, username=u.username, email=u.email, password=u.password) for u in users]

    def update_user(self, id:int, user_dto: UserUpdateDto):
        user = self._user_repository.get_by_id(id)
        user.username = user_dto.username
        updated_user = self._user_repository.save(user)
        return UserDto(id=updated_user.id, username=updated_user.username, email=updated_user.email, password=updated_user.password)

    def delete_user(self, id) -> None:
        return self._user_repository.delete(id)

    def _verify_password(self, plain: str, hashed: str):
        return self.pwd_context.verify(plain, hashed)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str):
        user = self._user_repository.get_by_username(username)
        if not user:
            return False
        if not self._verify_password(password, user.password):
            return False
        return user
