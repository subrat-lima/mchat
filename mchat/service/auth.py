import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException
from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
)

import mchat.data.user as d_user
from mchat.helper import db_connect, hash_password, match_password


@db_connect
def register(curs, in_user: HTTPBasicCredentials):
    db_user = d_user.get_by_username(curs, in_user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="user already exists")
    in_user.password = hash_password(in_user.password)
    d_user.add(curs, in_user)
    return {"status": True, "detail": "user registered"}


@db_connect
def login(curs, in_user: HTTPBasicCredentials):
    db_user = d_user.get_by_username(curs, in_user.username)
    if not db_user:
        raise HTTPException(status_code=404, detail="user not found")
    if not match_password(in_user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="invalid username or password")
    expire = datetime.now(timezone.utc) + timedelta(minutes=600)
    data = {"sub": in_user.username, "exp": expire}
    encoded_jwt = jwt.encode(data, os.getenv("SECRET_KEY"), algorithm="HS256")
    return {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "status": True,
        "detail": "login successful",
    }


@db_connect
def get_user_from_token(curs, token):
    payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
    username = payload.get("sub")
    if username is None:
        return None
    return d_user.get_by_username(curs, username)
