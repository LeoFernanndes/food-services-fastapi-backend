from application.base.base_dto import BaseDto


class BaseUserProfileDto(BaseDto):
    pass


class UserProfileCreateDto(BaseUserProfileDto):
    first_name: str
    last_name: str
    age: int
    profile_picture: str


class UserProfileDto(UserProfileCreateDto):
    id: int
    user_id: int


class UserProfileUpdateDto(BaseDto):
    first_name: str
    last_name: str
    age: int
    profile_picture: str
