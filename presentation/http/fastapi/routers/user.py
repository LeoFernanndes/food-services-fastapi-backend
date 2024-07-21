from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from application.authentication.dtos.user_dtos import UserCreateDto, UserUpdateDto
from application.authentication.services.user_service import UserService
from domain.authentication.repositories.exceptions import DatabaseIntegrityError
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
    try:
        create_user_dto = user_service.create_user(user)
        return JSONResponse(create_user_dto.model_dump(), status_code=201)
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except Exception as e:
        raise HTTPException(status_code=500)


@user_router.put("/{id}")
def update_user(id: int, user_dto: UserUpdateDto, user_service: UserService = Depends(get_user_service)):
    if not user_service.get_user_by_id(id):
        raise HTTPException(404)
    try:
        updated_user_dto = user_service.update_user(id, user_dto)
        return updated_user_dto
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except:
        raise HTTPException(status_code=500)


@user_router.delete("/{id}")
def delete_user(id: int, user_service: UserService = Depends(get_user_service)):
    if not user_service.get_user_by_id(id):
        raise HTTPException(404)
    user_service.delete_user_by_id(id)
    return JSONResponse(content=None, status_code=204)
