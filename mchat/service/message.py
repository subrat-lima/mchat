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
import mchat.data.message as d_message
import mchat.data.user as d_user
import mchat.model.chat as m_chat
import mchat.model.contact as m_contact
import mchat.model.member as m_member
import mchat.model.message as m_message
import mchat.model.token as m_token
import mchat.model.user as m_user
import mchat.service.message as s_message
from mchat.model import db_connect


@db_connect
def add(curs, message: m_message.Message) -> bool:
    db_message = d_message.create(curs, message)
    if not db_message:
        raise HTTPException(status_code=400, detail="error adding message")
    return True


@db_connect
def get_all(
    curs, current_user: m_user.User, chat_id: int
) -> Optional[list[m_message.Message]]:
    return d_message.get_all_in_chat(curs, chat_id)
