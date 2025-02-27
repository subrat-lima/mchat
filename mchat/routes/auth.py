from fastapi import APIRouter

import mchat.service.auth as service
from mchat.model import SuccessHandler, Token, User, UserIn
from mchat.service.auth import LoginUserForm

router = APIRouter()


@router.post("/register")
async def register(user: UserIn):
    return service.register(user)


@router.post("/login")
async def login(user: LoginUserForm) -> Token:
    return service.login(user)
