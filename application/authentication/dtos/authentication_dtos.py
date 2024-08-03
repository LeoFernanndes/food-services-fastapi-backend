from pydantic import BaseModel


class TokenPairResponseDto(BaseModel):
    access_token: str
    refresh_token: str
    token_duration_minutes: int
    refresh_token_duration_minutes: int
    token_type: str


class TokenData(BaseModel):
    username: str
    email: str
