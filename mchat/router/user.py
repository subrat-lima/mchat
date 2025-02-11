from typing import Annotated

from fastapi import APIRouter, Depends

from mchat.model import (
    User,
    UserPublic,
    get_all_users,
    get_current_user,
)

router = APIRouter(prefix="/users")


@router.get("/", response_model=list[UserPublic])
async def get_all() -> list[UserPublic]:
    return get_all_users()


@router.get("/me", response_model=UserPublic)
async def me(current_user: Annotated[User, Depends(get_current_user)]) -> UserPublic:
    return current_user
