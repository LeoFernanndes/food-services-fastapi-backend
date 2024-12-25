from dotenv import load_dotenv
from typing import List

from application.account_management.dtos.user_profile_dtos import UserProfileCreateDto, UserProfileDto, UserProfileUpdateDto
from application.base import exceptions as application_exceptions
from domain.account_management.entities.user_profile import UserProfile
from domain.account_management.repositories.user_profile_repository import UserProfileRepository
from domain.authentication.repositories.user_repository import UserRepository


load_dotenv()


class UserProfileService:
    def __init__(self, user_profile_respository: UserProfileRepository, user_repository: UserRepository):
        self._user_profile_repository = user_profile_respository
        self._user_repository = user_repository

    def create_user_profile(self, user_profile_create_dto: UserProfileCreateDto, user_id: int) -> UserProfileDto:
        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise application_exceptions.EntityNotFoundApplicationException(f'User not found')

        user_profile = UserProfile(
            id=None,
            first_name=user_profile_create_dto.first_name,
            last_name=user_profile_create_dto.last_name,
            age=user_profile_create_dto.age,
            profile_picture=user_profile_create_dto.profile_picture,
            user_id=user.id
        )
        new_user_profile = self._user_profile_repository.save(user_profile)
        return UserProfileDto(
            id=new_user_profile.id,
            first_name=new_user_profile.first_name,
            last_name=new_user_profile.last_name,
            age=new_user_profile.age,
            profile_picture=new_user_profile.profile_picture,
            user_id=user.id
        )

    def delete_user_profile(self, user_profile_id) -> None:
        return self._user_profile_repository.delete(user_profile_id)

    def get_user_profile_by_id(self, user_profile_id: int) -> UserProfileDto | None:
        user_profile = self._user_profile_repository.get_by_id(user_profile_id)
        if not user_profile:
            return None
        return UserProfileDto(
            id=user_profile.id,
            first_name=user_profile.first_name,
            last_name=user_profile.last_name,
            age=user_profile.age,
            profile_picture=user_profile.profile_picture,
            user_id=user_profile.user_id
        )

    def list_user_profiles_by_user_id(self, user_id: int) -> List[UserProfileDto]:
        user_profiles = self._user_profile_repository.get_by_user_id(user_id)
        return [
            UserProfileDto(
                id=user_profile.id,
                first_name=user_profile.first_name,
                last_name=user_profile.last_name,
                age=user_profile.age,
                profile_picture=user_profile.profile_picture,
                user_id=user_profile.user_id
            ) for user_profile in user_profiles
        ]

    def update_user_profile(self, id: int, user_profile_update_dto: UserProfileUpdateDto) -> UserProfileDto:
        user_profile = self._user_profile_repository.get_by_id(id)
        user_profile.first_name = user_profile_update_dto.first_name
        user_profile.last_name = user_profile_update_dto.last_name
        user_profile.age = user_profile_update_dto.age
        user_profile.profile_picture = user_profile_update_dto.profile_picture
        updated_user_profile = self._user_profile_repository.save(user_profile)
        return UserProfileDto(
            id=updated_user_profile.id,
            first_name=updated_user_profile.first_name,
            last_name=updated_user_profile.last_name,
            age=updated_user_profile.age,
            profile_picture=updated_user_profile.profile_picture,
            user_id=updated_user_profile.user_id
        )
