from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    password: str
    is_active: bool


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
