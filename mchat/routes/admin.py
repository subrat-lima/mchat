from typing import Optional

from fastapi import APIRouter

import mchat.service.admin as s_admin
from mchat.model import Chat, Group, Message, MessageRecipient, User, UserGroup
from mchat.service.auth import CurrentUser

router = APIRouter(prefix="/admin")


@router.get("/users")
async def get_users(current_user: CurrentUser) -> Optional[list[User]]:
    return s_admin.get_users(current_user)


@router.get("/groups")
async def get_groups(current_user: CurrentUser) -> Optional[list[Group]]:
    return s_admin.get_groups(current_user)


@router.get("/user_groups")
async def get_user_groups(current_user: CurrentUser) -> Optional[list[UserGroup]]:
    return s_admin.get_user_groups(current_user)


@router.get("/messages")
async def get_messages(current_user: CurrentUser) -> Optional[list[Message]]:
    return s_admin.get_messages(current_user)


@router.get("/message_recipients")
async def get_messages(current_user: CurrentUser) -> Optional[list[MessageRecipient]]:
    return s_admin.get_message_recipients(current_user)
