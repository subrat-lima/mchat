from pydantic import BaseModel


class Contact(BaseModel):
    user_id: int
    friend_id: int
    alias: str
