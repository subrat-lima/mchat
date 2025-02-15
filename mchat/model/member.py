from datetime import datetime

from pydantic import BaseModel


class Member(BaseModel):
    chat_id: int
    user_id: int
    role_id: int
    joined_at: str | None = f"{datetime.now()}"
    left_at: str | None = None
