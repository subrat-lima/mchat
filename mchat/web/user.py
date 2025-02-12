from typing import Optional

from fastapi import APIRouter

import mchat.model.user as m_user
import mchat.service.user as s_user

router = APIRouter(prefix="/users")


@router.get("/", response_model=Optional[list[m_user.UserOut]])
async def get_all() -> Optional[list[m_user.UserOut]]:
    return s_user.get_all()


@router.get("/me", response_model=m_user.UserOut)
async def get_me(current_user: s_user.CurrentUser) -> m_user.UserOut:
    return current_user
