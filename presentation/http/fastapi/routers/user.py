from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException

from application.authentication.dtos.user_dtos import UserCreateDto, UserUpdateDto
from application.authentication.services.user_service import UserService
from presentation.dependencies import get_user_service


user_router = APIRouter()


@user_router.get("/{id}")
def get_user(id: int, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user_by_id(id)
    if not user:
        raise HTTPException(status_code=404)
    return user


@user_router.get("/")
def get_users(user_service: UserService = Depends(get_user_service), items_per_page: int = Query(1000, ge=0), page: int = Query(0, ge=0)):
    return user_service.get_all_users(items_per_page, page)


@user_router.post("/")
def create_user(user: UserCreateDto, user_service: UserService = Depends(get_user_service)):
    create_user_dto = user_service.create_user(user)
    return create_user_dto


@user_router.put("/{id}")
def update_user(id: int, user_dto: UserUpdateDto, user_service: UserService = Depends(get_user_service)):
    if not user_service.get_user_by_id(id):
        raise HTTPException(404)
    updated_user_dto = user_service.update_user(id, user_dto)
    return updated_user_dto
