import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

import mchat.data.chat as d_chat
import mchat.data.contact as d_contact
import mchat.data.member as d_member
import mchat.data.user as d_user
import mchat.model.chat as m_chat
import mchat.model.contact as m_contact
import mchat.model.member as m_member
import mchat.model.token as m_token
import mchat.model.user as m_user
from mchat.model import db_connect


@db_connect
def add(curs, user: m_user.User, chat_id: int, contact_id: int) -> bool:
    member = d_member.get_one(chat_id, contact_id)
    if member:
        raise HTTPException(status_code=400, detail="member already exists")
    member_1 = m_member.Member(chat_id=chat_id, user_id=user.id, role_id=2)
    db_member_1 = d_member.create(curs, member_1)
    if not db_member_1:
        raise HTTPException(status_code=400, detail="error adding member")
    return True


@db_connect
def get_all(curs, user: m_user.User, chat_id: int) -> Optional[list[m_member.Member]]:
    return d_member.get_all_in_chat(curs, chat_id)
