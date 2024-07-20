import jwt
import os

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv

from domain.authentication.repositories.user_repository import UserRepository


load_dotenv()


class AuthenticationService:
    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    # to get a string like this run:
    # openssl rand -hex 32
    SECRET_KEY = os.getenv("PASSWORD_HASHING_SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def create_access_token(self, data: dict, expire_delta: timedelta):
        to_encode = data.copy()
        if expire_delta:
            expire = datetime.now(timezone.utc) + expire_delta
        else:
            expire = datetime.now(timedelta.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
