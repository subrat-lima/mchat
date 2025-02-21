from pydantic import BaseModel


class SuccessHandler(BaseModel):
    status_code: int = 200
    detail: str


class User(BaseModel):
    id: int
    username: str
    password: str
    create_date: str
    is_active: bool


class UserIn(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    username: str
