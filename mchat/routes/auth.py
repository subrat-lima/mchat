from fastapi import APIRouter

import mchat.service.auth as service
from mchat.model import SuccessHandler, Token, User, UserIn

router = APIRouter()


@router.post("/register")
async def register(user: UserIn) -> SuccessHandler:
    return service.register(user)


@router.post("/login")
async def login(user: service.LoginUserForm) -> Token:
    return service.login(user)
