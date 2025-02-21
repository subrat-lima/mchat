from typing import Optional

from fastapi import APIRouter

import mchat.model.contact as m_contact
import mchat.service.contact as s_contact
import mchat.service.user as s_user

router = APIRouter(prefix="/contacts")


@router.get("/", response_model=Optional[list[m_contact.Contact]])
async def get_all(
    current_user: s_user.CurrentUser,
) -> Optional[list[m_contact.Contact]]:
    return s_contact.get_all(current_user)


@router.post("/add")
async def add(current_user: s_user.CurrentUser, contact: m_contact.ContactIn) -> bool:
    return s_contact.add(current_user, contact)
