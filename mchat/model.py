from typing import Optional

from pydantic import BaseModel


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


class Chat(BaseModel):
    recipient_id: Optional[int] = None
    name: str
    message: Optional[str] = None
    message_create_date: Optional[str] = None

    def __hash__(self):
        recipient_id = self.recipient_id
        data = hash(f"{recipient_id}")
        return data

    def __eq__(self, other):
        r1_id = self.recipient_id if self.recipient_id else 0
        r1_gid = self.recipient_group_id if self.recipient_group_id else 0
        r2_id = other.recipient_id if other.recipient_id else 0
        r2_gid = other.recipient_group_id if other.recipient_group_id else 0
        if r1_id != r2_id:
            return False
        if r1_gid != r2_gid:
            return False
        return True

    def __lt__(self, other):
        s_date = self.message_create_date if self.message_create_date else ""
        o_date = other.message_create_date if other.message_create_date else ""
        return s_date < o_date


class MessageIn(BaseModel):
    message: str
    category: int
    parent_message_id: Optional[int] = None
    recipient_id: Optional[int] = None
    recipient_group_id: Optional[int] = None


class Message(BaseModel):
    id: int
    message: str
    category: int
    sender_id: int
    parent_message_id: Optional[int] = None
    create_date: str
    expiry_date: Optional[str] = None


class MessageOut(BaseModel):
    id: int
    group_id: Optional[int] = None
    chat_type: str = "direct"
    message: str
    sender_id: int
    create_date: str
    sender_name: str

    def __hash__(self):
        gid = self.group_id
        if gid is None:
            gid = 0
        return hash(
            f"{self.id}-{self.chat_type}-{gid}-{self.sender_id}-{self.create_date}"
        )

    def __eq__(self, other):
        r1_gid = self.group_id if self.group_id else 0
        r2_gid = other.group_id if other.group_id else 0
        return (
            r1_gid == r2_gid
            and self.id == other.id
            and self.chat_type == other.chat_type
            and self.sender_id == other.sender_id
            and self.create_date == other.create_date
        )

    def __lt__(self, other):
        return self.create_date < other.create_date
