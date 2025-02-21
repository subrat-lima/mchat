from typing import Optional

from fastapi import APIRouter

import mchat.model.chat as m_chat
import mchat.model.contact as m_contact
import mchat.model.member as m_member
import mchat.model.message as m_message
import mchat.service.chat as s_chat
import mchat.service.contact as s_contact
import mchat.service.member as s_member
import mchat.service.message as s_message
import mchat.service.user as s_user

router = APIRouter(prefix="/chat")


@router.get("/{chat_id}/message")
async def get_all(
    current_user: s_user.CurrentUser, chat_id: int
) -> Optional[list[m_message.Message]]:
    return s_message.get_all(current_user, chat_id)


@router.post("/{chat_id}/message")
async def add(
    current_user: s_user.CurrentUser, chat_id: int, in_message: m_message.MessageIn
) -> bool:
    message = m_message.Message(
        chat_id=chat_id,
        user_id=current_user.id,
        content_type_id=in_message.content_type_id,
        content=in_message.content,
    )
    return s_message.add(message)
