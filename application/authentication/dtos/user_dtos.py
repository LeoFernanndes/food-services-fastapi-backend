from application.base.base_dto import BaseDto


class BaseUserDto(BaseDto):
    username: str


class UserCreateDto(BaseUserDto):
    email: str
    password: str


class UserDto(BaseUserDto):
    id: int
    email: str


class UserUpdateDto(BaseUserDto):
    pass

