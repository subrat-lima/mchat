from typing import Optional

from fastapi import APIRouter

import mchat.model.chat as m_chat
import mchat.model.contact as m_contact
import mchat.service.chat as s_chat
import mchat.service.contact as s_contact
import mchat.service.user as s_user

router = APIRouter(prefix="/chat")


@router.get("/", response_model=Optional[list[m_chat.ChatOut]])
async def get_all(
    current_user: s_user.CurrentUser,
) -> Optional[list[m_contact.Contact]]:
    return s_chat.get_all(current_user)


@router.post("/add_direct")
async def add_direct(current_user: s_user.CurrentUser, contact_id: int) -> bool:
    return s_chat.add_direct(current_user, contact_id)
