from fastapi import APIRouter

import mchat.model.token as m_token
import mchat.model.user as m_user
import mchat.service.user as s_user

router = APIRouter()


@router.post("/register")
async def register(user: m_user.UserIn) -> bool:
    return s_user.register(user)


@router.post("/login")
async def login(user: s_user.LoginUserForm) -> m_token.Token:
    return s_user.login(user)
