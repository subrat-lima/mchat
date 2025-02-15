from pydantic import BaseModel


class ContentType(BaseModel):
    id: int
    name: str


class Message(BaseModel):
    id: int | None = None
    chat_id: int
    user_id: int
    content_type_id: int
    content: str


class MessageIn(BaseModel):
    content_type_id: int
    content: str
