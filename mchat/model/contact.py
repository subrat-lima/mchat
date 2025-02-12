from pydantic import BaseModel


class Contact(BaseModel):
    user_id: int
    friend_id: int
    alias: str


class ContactIn(BaseModel):
    username: str
    alias: str


class ContactOut(BaseModel):
    username: str
    alias: str
