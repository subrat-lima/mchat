from typing import Optional

from pydantic import BaseModel


class SuccessHandler(BaseModel):
    status_code: int = 200
    detail: str
    data: Optional[dict] = {}


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


class GroupIn(BaseModel):
    name: str


class Group(BaseModel):
    id: int
    name: str
    owner_id: int
    create_date: str
    is_active: int


class UserGroupIn(BaseModel):
    group_id: int
    user_id: int
    role: int = 0


class UserGroup(BaseModel):
    id: int
    user_id: int
    group_id: int
    role: int
    create_date: str
    is_active: int
