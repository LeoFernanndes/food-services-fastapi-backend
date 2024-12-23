from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse, Response

from application.authentication.dtos.user_dtos import UserCreateDto, UserUpdateDto, UserDto
from application.authentication.services.user_service import UserService
from application.account_management.dtos.user_profile_dtos import UserProfileDto, UserProfileCreateDto, UserProfileUpdateDto
from application.account_management.services.user_profile_service import UserProfileService
from domain.authentication.repositories.exceptions import DatabaseIntegrityError
from presentation.dependencies import get_user_service, get_user_profile_service


user_router = APIRouter()


@user_router.get("/{user_id}")
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)) -> UserDto:
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user


@user_router.get("/")
def get_users(user_service: UserService = Depends(get_user_service), items_per_page: int = Query(1000, ge=0), page: int = Query(0, ge=0)) -> List[UserDto]:
    return user_service.get_all_users(items_per_page, page)


@user_router.post("/")
def create_user(user: UserCreateDto, user_service: UserService = Depends(get_user_service)) -> UserDto:
    try:
        create_user_dto = user_service.create_user(user)
        return JSONResponse(create_user_dto.model_dump(), status_code=201)
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except Exception as e:
        raise HTTPException(status_code=500)


@user_router.put("/{user_id}")
def update_user(user_id: int, user_dto: UserUpdateDto, user_service: UserService = Depends(get_user_service)) -> UserDto:
    if not user_service.get_user_by_id(user_id):
        raise HTTPException(404)
    try:
        updated_user_dto = user_service.update_user(user_id, user_dto)
        return updated_user_dto
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except:
        raise HTTPException(status_code=500)


@user_router.delete("/{user_id}")
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    if not user_service.get_user_by_id(user_id):
        raise HTTPException(404)
    user_service.delete_user_by_id(user_id)
    return JSONResponse(content={}, status_code=204)


@user_router.post("/{user_id}/user-profiles/")
def create_user_profile(
        user_id: int,
        user_profile_create_dto: UserProfileCreateDto,
        user_service: UserService = Depends(get_user_service),
        user_profile_service: UserProfileService = Depends(get_user_profile_service)
    ) -> UserProfileDto:
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    try:
        user_profile_dto = user_profile_service.create_user_profile(user_profile_create_dto, user_id)
        return JSONResponse(user_profile_dto.model_dump(), status_code=201)
    except DatabaseIntegrityError as e:
        raise HTTPException(status_code=400, detail=e.args)
    except Exception as e:
        raise HTTPException(status_code=500)


@user_router.delete("/{user_id}/user-profiles/{user_profile_id}")
def delete_user_profile(
            user_id: int,
            user_profile_id: int,
            user_profile_service: UserProfileService = Depends(get_user_profile_service),
            user_service: UserService = Depends(get_user_service)
        ):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    user_profile = user_profile_service.get_user_profile_by_id(user_profile_id)
    if not user_profile:
        raise HTTPException(status_code=404)
    user_profile_service.delete_user_profile(user_profile_id)
    return Response(status_code=204)


@user_router.get("/{user_id}/user-profiles/{user_profile_id}")
def get_user_profile(
        user_id: int,
        user_profile_id: int,
        user_profile_service: UserProfileService = Depends(get_user_profile_service),
        user_service: UserService = Depends(get_user_service)
        ):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    user_profile = user_profile_service.get_user_profile_by_id(user_profile_id)
    if not user_profile:
        raise HTTPException(status_code=404)
    return user_profile


@user_router.get("/{user_id}/user-profiles/")
def list_user_profiles(
        user_id: int,
        user_service: UserService = Depends(get_user_service),
        user_profile_service: UserProfileService = Depends(get_user_profile_service)
    ) -> List[UserProfileDto]:
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user_profile_service.list_user_profiles_by_user_id(user_id)


@user_router.put("/{user_id}/user-profiles/{user_profile_id}")
def update_user_profile(
        user_id: int,
        user_profile_id: int,
        user_profile_update_dto: UserProfileUpdateDto,
        user_profile_service: UserProfileService = Depends(get_user_profile_service),
        user_service: UserService = Depends(get_user_service)
    ) -> UserProfileDto:
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404)
    user_user_profiles = user_profile_service.list_user_profiles_by_user_id(user_id)
    if user_profile_id not in [user_profile.id for user_profile in user_user_profiles]:
        raise HTTPException(status_code=404)
    try:
        return user_profile_service.update_user_profile(user_profile_id, user_profile_update_dto)
    except Exception as e:
        raise HTTPException(status_code=500)
