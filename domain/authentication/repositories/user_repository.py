from abc import ABC, abstractmethod
from typing import List

from domain.authentication.entities.user import User


class UserRepository(ABC):

    @abstractmethod
    def get_by_id(self, id: int) -> User | None:
        pass

    @abstractmethod
    def get_all(self, limit: int = 1000, offset: int = 0) -> List[User]:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass
