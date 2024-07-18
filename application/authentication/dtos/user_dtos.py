from application.base.base_dto import BaseDto


class BaseUserDto(BaseDto):
    username: str


class UserCreateDto(BaseUserDto):
    email: str
    password: str


class UserDto(UserCreateDto):
    id: int


class UserUpdateDto(BaseUserDto):
    pass

