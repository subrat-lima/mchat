from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    chat_type_id: int


class ChatType(BaseModel):
    id: int
    name: str
