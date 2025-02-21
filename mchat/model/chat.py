from pydantic import BaseModel


class Chat(BaseModel):
    id: int
    chat_type_id: int


class ChatType(BaseModel):
    id: int
    name: str


class ChatOut(Chat):
    pass
    # user_id: int
    # alias: str


class DirectChat(BaseModel):
    id: int
    user_id_1: int
    user_id_2: int


class DirectChatOut(BaseModel):
    id: int
    username: int
