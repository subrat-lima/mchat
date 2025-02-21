from typing import Optional

from fastapi import APIRouter

import mchat.service.chat as s_chat
from mchat.model import GroupIn, UserGroupIn
from mchat.service.auth import CurrentUser

router = APIRouter(prefix="/chats")


@router.post("/groups/")
async def add_group(current_user: CurrentUser, group: GroupIn):
    return s_chat.add_group(current_user, group)


@router.post("/user_groups/")
async def add_user_group(current_user: CurrentUser, user_group: UserGroupIn):
    return s_chat.add_user_group(current_user, user_group)


# @router.get("/", response_model=Optional[list[ChatOut]])
# @router.get("/")
# async def get_all(current_user: CurrentUser):
# return s_chat.get_all(current_user)
