import jwt
import redis

from datetime import timedelta
from fastapi import APIRouter, Depends, status, Header
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from typing import Annotated

from application.authentication.services.authentication_service import AuthenticationService
from application.authentication.dtos.authentication_dtos import TokenPairResponseDto, TokenData
from application.authentication.services.user_service import UserService
from domain.authentication.entities.user import User
from infrastructure.cache.redis import redis_client
from presentation.dependencies import get_authentication_service, get_user_service


auth_router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
)


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        auth_service: Annotated[AuthenticationService, Depends(get_authentication_service)]
    ):
    try:
        return auth_service.decode_access_token(access_token=token)
    except:
        raise credentials_exception


@auth_router.post("/token")
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: Annotated[UserService, Depends(get_user_service)],
        auth_service: Annotated[AuthenticationService, Depends(get_authentication_service)]
        ) -> TokenPairResponseDto:
    if not user_service.check_password_is_valid(form_data.username, form_data.password):
        raise credentials_exception
    user = user_service.get_user_by_username(form_data.username)
    return auth_service.create_token_pair(TokenData(username=user.username, email=user.email))


@auth_router.post("/refresh")
def refresh_auth_and_refresh_tokens(
        refresh: Annotated[str, Header()],
        auth_service: Annotated[AuthenticationService, Depends(get_authentication_service)]
        ) -> TokenPairResponseDto:
    try:
        token_data = auth_service.decode_refresh_token(refresh)
    except:
        raise credentials_exception
    return auth_service.refresh_token_pair(token_data, refresh)


@auth_router.get("/me")
def who_am_i(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
