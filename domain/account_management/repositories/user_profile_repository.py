from abc import ABC, abstractmethod
from typing import List

from domain.account_management.entities.user_profile import UserProfile


class UserProfileRepository(ABC):

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

    @abstractmethod
    def get_all(self, limit: int = 1000, offset: int = 0) -> List[UserProfile]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> UserProfile | None:
        pass

    @abstractmethod
    def get_by_user_id(self, id) -> List[UserProfile]:
        pass

    @abstractmethod
    def save(self, user_profile: UserProfile) -> UserProfile:
        pass
