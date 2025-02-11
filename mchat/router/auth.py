from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from mchat.model import (
    Token,
    UserLogin,
    UserRegister,
    generate_token,
    login_user,
    register_user,
)

router = APIRouter()


@router.post("/register")
async def register(user: UserRegister):
    status = register_user(user)
    return {"status": status, "message": "user registered"}


@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = UserLogin(username=form_data.username, password=form_data.password)
    db_user = login_user(user)
    return generate_token(db_user)
