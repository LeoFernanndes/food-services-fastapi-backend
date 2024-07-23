import jwt
import os

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from application.authentication.dtos.authentication_dtos import TokenData, TokenPairResponseDto
from domain.authentication.repositories.user_repository import UserRepository


load_dotenv()


class AuthenticationService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    SECRET_KEY = os.getenv("PASSWORD_HASHING_SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
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

    def decode_access_token(self, access_token: str) -> TokenData:
        payload = jwt.decode(access_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise Exception("Username not contained in token.")
        user = self._user_repository.get_by_username(username)
        if not user:
            raise Exception("User not found.")
        return TokenData(username=username, email=user.email)

    def decode_refresh_token(self, refresh_token: str) -> TokenData:
        payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        username: str = payload.get("sub")
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