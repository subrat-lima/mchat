from typing import Optional

from fastapi import APIRouter

import mchat.service.chat as s_chat
from mchat.model import Chat, GroupIn, Message, MessageIn, MessageOut, UserGroupIn
from mchat.service.auth import CurrentUser

router = APIRouter(prefix="/chats")


@router.post("/groups/")
async def add_group(current_user: CurrentUser, group: GroupIn):
    return s_chat.add_group(current_user, group)


@router.post("/user_groups/")
async def add_user_group(current_user: CurrentUser, user_group: UserGroupIn):
    return s_chat.add_user_group(current_user, user_group)


@router.post("/messages")
async def add_message(current_user: CurrentUser, message: MessageIn):
    return s_chat.add_message(current_user, message)


@router.get("/")
async def get_chats(current_user: CurrentUser) -> Optional[list[Chat]]:
    return s_chat.get_chats(current_user)


@router.get("/messages/{chat_type}/{chat_id}")
async def get_messages(
    current_user: CurrentUser, chat_type: str, chat_id: int
) -> Optional[list[MessageOut]]:
    return s_chat.get_messages(current_user, chat_type, chat_id)
