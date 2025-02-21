from typing import Optional

from fastapi import APIRouter

import mchat.model.chat as m_chat
import mchat.model.contact as m_contact
import mchat.model.member as m_member
import mchat.service.chat as s_chat
import mchat.service.contact as s_contact
import mchat.service.member as s_member
import mchat.service.user as s_user

router = APIRouter(prefix="/member")


@router.post("/add")
async def add_direct(
    current_user: s_user.CurrentUser, chat_id: int, contact_id: int
) -> bool:
    return s_chat.add(current_user, chat_id, contact_id)


@router.post("/get_all")
async def get_all(
    current_user: s_user.CurrentUser, chat_id: int
) -> Optional[list[m_member.Member]]:
    return s_member.get_all(current_user, chat_id)
