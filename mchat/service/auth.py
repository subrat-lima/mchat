import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

import mchat.data.user as d_user
from mchat.helper import db_connect, hash_password, match_password
from mchat.model import SuccessHandler, Token, TokenData, User, UserIn

LoginUserForm = Annotated[OAuth2PasswordRequestForm, Depends()]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@db_connect
def register(curs, in_user: UserIn):
    db_user = d_user.get_by_username(curs, in_user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="user already exists")
    in_user.password = hash_password(in_user.password)
    d_user.add(curs, in_user)
    return {"status": 200, "message": "user registered"}


@db_connect
def login(curs, in_user: LoginUserForm) -> Token:
    db_user = d_user.get_by_username(curs, in_user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    if not match_password(in_user.password, db_user.password):
        raise HTTPException(status_code=400, detail="invalid username or password")
    expire = datetime.now(timezone.utc) + timedelta(minutes=600)
    data = {"sub": db_user.username, "exp": expire}
    encoded_jwt = jwt.encode(data, os.getenv("SECRET_KEY"), algorithm="HS256")
    return Token(access_token=encoded_jwt)


@db_connect
def get_user_from_token(curs, token) -> User:
    return d_user.get_by_username(curs, token.username)


def get_user(token):
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
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    db_user = get_user_from_token(token_data)
    if not db_user:
        raise credentials_exception
    return db_user


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
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
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    db_user = get_user_from_token(token_data)
    if not db_user:
        raise credentials_exception
    return db_user


CurrentUser = Annotated[User, Depends(get_current_user)]
