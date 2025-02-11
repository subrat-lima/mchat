import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from pydantic import AfterValidator, BaseModel, PlainSerializer
from sqlmodel import Field, Session, SQLModel, create_engine, select

load_dotenv()


engine = create_engine("sqlite:///mtodo.db")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True)
    password: str
    is_active: bool = False


class UserRegister(SQLModel):
    username: str
    password: str


class UserLogin(SQLModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: int
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def register_user(user: UserRegister) -> bool:
    global engine
    with Session(engine) as session:
        statement = select(User).where(User.username == user.username)
        db_user = session.exec(statement).one_or_none()
        if db_user:
            raise HTTPException(status_code=400, detail="user already exists")
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        session.add(User(username=user.username, password=hashed_password))
        session.commit()
    return True


def login_user(user: UserLogin) -> User:
    global engine
    with Session(engine) as session:
        statement = select(User).where(User.username == user.username)
        db_user = session.exec(statement).one_or_none()
        if db_user is None:
            raise HTTPException(status_code=404, detail="user not found")
        if bcrypt.checkpw(
            user.password.encode("utf-8"), db_user.password.encode("utf-8")
        ):
            return db_user
        raise HTTPException(
            status_code=400,
            detail="invalid username/password",
            headers={"WWW-Authenticate": "Bearer"},
        )


def generate_token(user: User) -> Token:
    global ACCESS_TOKEN_EXPIRE_MINUTES
    global SECRET_KEY
    global ALGORITHM
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    data = {"sub": user.username, "exp": expire}
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return Token(access_token=encoded_jwt, token_type="bearer")


def get_all_users() -> list[User]:
    global engine
    with Session(engine) as session:
        statement = select(User)
        users = session.exec(statement).all()
        return users


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    global engine
    global SECRET_KEY
    global ALGORITHM
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    with Session(engine) as session:
        statement = select(User).where(User.username == token_data.username)
        db_user = session.exec(statement).one_or_none()
        if db_user is None:
            raise credentials_exception
        return db_user


SQLModel.metadata.create_all(engine)
