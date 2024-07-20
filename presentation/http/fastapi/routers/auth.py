import jwt

from datetime import timedelta
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from typing import Annotated

from application.authentication.services.authentication_service import AuthenticationService
from application.authentication.dtos.authentication_dtos import Token, TokenData
from application.authentication.services.user_service import UserService
from domain.authentication.entities.user import User
from presentation.dependencies import get_authentication_service, get_user_service


auth_router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        user_service: Annotated[UserService, Depends(get_user_service)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, user_service.SECRET_KEY, algorithms=[user_service.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = user_service.get_user_by_username(username)
    if not user:
        raise credentials_exception
    return user


@auth_router.post("/token")
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        user_service: Annotated[UserService, Depends(get_user_service)],
        auth_service: Annotated[AuthenticationService, Depends(get_authentication_service)]
        ) -> Token:
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username of password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=user_service.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username}, expire_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/me")
def who_am_i(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
