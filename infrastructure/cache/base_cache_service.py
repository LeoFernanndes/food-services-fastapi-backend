from abc import ABC, abstractmethod
from typing import Union


class BaseCacheService(ABC):
    
    @abstractmethod
    def save_expirable_dict(self, hash_key: str, obj: dict, expiration_time_minutes: int) -> None:
        pass
    
    @abstractmethod
    def save_expirable_value(self, hash_key: str, value: Union[str, float], expiration_time_minutes: int) -> None:
        pass
    
    @abstractmethod
    def get_dict_key_value_from_cache(self, hash_key: str, key: str) -> Union[str, float]:
        pass

    @abstractmethod
    def get_complete_dict_from_cache(self, hash_key: str) -> dict:
        pass
    
    @abstractmethod
    def get_value_from_cache(self, hash_key: str) -> Union[str, float]:
        pass
    
    @abstractmethod
    def remove_from_cache(self, hash_key: str) -> None:
        pass
