import os

from datetime import datetime, timedelta, timezone

import jwt

from dotenv import load_dotenv

from application.authentication.dtos.authentication_dtos import TokenData, TokenPairResponseDto
from domain.authentication.repositories.user_repository import UserRepository
from infrastructure.cache.base_cache_service import BaseCacheService


load_dotenv()


class AuthenticationService:
    def __init__(self, user_repository: UserRepository, cache_service: BaseCacheService):
        self._user_repository = user_repository
        self._cache_service = cache_service

    SECRET_KEY = os.getenv("PASSWORD_HASHING_SECRET_KEY")
    ALGORITHM = "HS256"
    OTP_EXPIRE_MINUTES = 5
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_MINUTES = 360

    def create_token_pair(self, token_data: TokenData) -> TokenPairResponseDto:
        access_token = self._create_access_token(token_data)
        refresh_token = self._create_refresh_token(token_data)
        return TokenPairResponseDto(
            access_token=access_token,
            token_duration_minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES,
            refresh_token=refresh_token,
            refresh_token_duration_minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES,
            token_type="bearer"
        )

    def refresh_token_pair(self, token_data: TokenData, used_refresh_token: str) -> TokenPairResponseDto:
        tokens = self.create_token_pair(token_data)
        self._add_tokens_to_rotation(tokens.access_token,tokens.refresh_token, used_refresh_token)
        return tokens

    def decode_access_token(self, access_token: str) -> TokenData:
        if not self._check_access_token_is_valid(access_token):
            raise Exception("Revoked token")
        payload = jwt.decode(access_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise Exception("Username not contained in token.")
        user = self._user_repository.get_by_username(username)
        if not user:
            raise Exception("User not found.")
        return TokenData(username=username, email=user.email)

    def decode_refresh_token(self, refresh_token: str) -> TokenData:
        if not self._check_refresh_token_was_never_used(refresh_token):
            raise Exception("Token already used.")
        if not self._check_refresh_token_is_valid(refresh_token):
            raise Exception("Revoked token")
        payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        username = payload.get("username")
        if username is None:
            raise Exception("Username not contained in token.")
        user = self._user_repository.get_by_username(username)
        if not user:
            raise Exception("User not found.")
        return TokenData(username=username, email=user.email)

    def _create_access_token(self, token_data: TokenData) -> str:
        token_data_to_be_encoded = token_data.model_dump()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data_to_be_encoded.update({"exp": expire})  # required format to be used from jwt library
        encoded_jwt = jwt.encode(token_data_to_be_encoded, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def _create_refresh_token(self, token_data: TokenData) -> str:
        token_data_to_be_encoded = token_data.model_dump()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)
        token_data_to_be_encoded.update({"exp": expire})  # required format to be used from jwt library
        encoded_jwt = jwt.encode(token_data_to_be_encoded, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def _check_refresh_token_was_never_used(self, refresh_token):
        token_pair_in_cache = self._cache_service.get_complete_dict_from_cache(refresh_token)
        if token_pair_in_cache:
            self._invalidate_access_token(token_pair_in_cache['access_token'])
            self._invalidate_refresh_token(token_pair_in_cache['refresh_token'])
            return False
        return True

    def _add_tokens_to_rotation(self, access_token, refresh_token, used_refresh_token):
        mapping = {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        self._cache_service.save_expirable_dict(used_refresh_token, mapping, self.REFRESH_TOKEN_EXPIRE_MINUTES * 60)

    def _invalidate_access_token(self, access_token):
        key = f"violated_access_token_{access_token}"
        self._cache_service.save_expirable_value(key, "value", self.ACCESS_TOKEN_EXPIRE_MINUTES)

    def _invalidate_refresh_token(self, refresh_token):
        key = f"violated_refresh_token_{refresh_token}"
        self._cache_service.save_expirable_value(key, "value", self.REFRESH_TOKEN_EXPIRE_MINUTES)

    def _check_access_token_is_valid(self, access_token: str) -> bool:
        key = f"violated_access_token_{access_token}"
        if self._cache_service.get_value_from_cache(key):
            return False
        return True

    def _check_refresh_token_is_valid(self, refresh_token: str) -> bool:
        key = f"violated_refresh_token_{refresh_token}"
        if self._cache_service.get_value_from_cache(key):
            return False
        return True
