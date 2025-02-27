from fastapi import APIRouter
from fastapi.security import HTTPBasicCredentials

import mchat.service.auth as service
from mchat.model import Token, User, UserIn

router = APIRouter()


@router.post("/register")
async def register(user: UserIn):
    return service.register(user)


@router.post("/login")
async def login(user: HTTPBasicCredentials) -> Token:
    return service.login(user)
