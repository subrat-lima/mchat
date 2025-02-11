import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

import mchat.data.user as d_user
import mchat.model.token as m_token
import mchat.model.user as m_user

LoginUserForm = Annotated[OAuth2PasswordRequestForm, Depends()]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def match_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def register(in_user: m_user.UserIn) -> bool:
    db_user = d_user.get_by_username(in_user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="user already exists")
    hashed_password = hash_password(in_user.password)
    user = m_user.User(username=in_user.username, password=hashed_password)
    return d_user.create(user)


def login(in_user: LoginUserForm) -> m_token.Token:
    db_user = d_user.get_by_username(in_user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    if not match_password(in_user.password, db_user.password):
        raise HTTPException(status_code=400, detail="invalid username or password")
    expire = datetime.now(timezone.utc) + timedelta(minutes=600)
    data = {"sub": db_user.username, "exp": expire}
    encoded_jwt = jwt.encode(data, os.getenv("SECRET_KEY"), algorithm="HS256")
    return m_token.Token(access_token=encoded_jwt)


def get_all() -> list[m_user.User]:
    return d_user.get_all()


async def get_me(token: Annotated[str, Depends(oauth2_scheme)]) -> m_user.User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = m_token.TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    db_user = d_user.get_by_username(token_data.username)
    if not db_user:
        raise credentials_exception
    return db_user


CurrentUser = Annotated[m_user.User, Depends(get_me)]
