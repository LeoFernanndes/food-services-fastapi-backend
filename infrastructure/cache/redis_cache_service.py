from typing import Union

from dotenv import load_dotenv
from redis import Redis

from infrastructure.cache.base_cache_service import BaseCacheService


load_dotenv()


class RedisCacheService(BaseCacheService):

    def __init__(self, redis_client: Redis):
        self._redis_client = redis_client

    def get_complete_dict_from_cache(self, hash_key: str) -> dict:
        return self._redis_client.hgetall(name=hash_key)

    def get_dict_key_value_from_cache(self, hash_key: str, key: str) -> Union[str, float]:
        return self._redis_client.hget(name=hash_key, key=key)

    def get_value_from_cache(self, hash_key: str) -> Union[str, float]:
        return self._redis_client.get(name=hash_key)

    def remove_from_cache(self, hash_key: str) -> None:
        self._redis_client.delete(hash_key)

    def save_expirable_dict(self, hash_key: str, obj: dict, expiration_time_minutes: int) -> None:
        self._redis_client.hset(name=hash_key, mapping=obj)
        self._redis_client.expire(name=hash_key, time=expiration_time_minutes * 60)

    def save_expirable_value(self, hash_key: str, value: Union[str, float], expiration_time_minutes: int) -> None:
        self._redis_client.set(name=hash_key, value=value, ex=expiration_time_minutes * 60)
