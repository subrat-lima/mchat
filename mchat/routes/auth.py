from fastapi import APIRouter
from fastapi.security import HTTPBasicCredentials

import mchat.service.auth as service
from mchat.model import Token

router = APIRouter()


@router.post("/register")
async def register(user: HTTPBasicCredentials):
    return service.register(user)


@router.post("/login")
async def login(user: HTTPBasicCredentials):
    return service.login(user)
