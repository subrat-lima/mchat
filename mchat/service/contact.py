import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

import mchat.data.contact as d_contact
import mchat.data.user as d_user
import mchat.model.contact as m_contact
import mchat.model.token as m_token
import mchat.model.user as m_user
from mchat.model import db_connect


@db_connect
def add(curs, user: m_user.User, in_contact: m_contact.ContactIn) -> bool:
    contact_user = d_user.get_by_username(curs, in_contact.username)
    db_contact = d_contact.get_one(curs, user.id, contact_user.id)
    if db_contact:
        raise HTTPException(status_code=400, detail="contact already exists")
    db_alias = d_contact.get_one_by_alias(curs, user.id, in_contact.alias)
    if db_alias:
        raise HTTPException(status_code=400, detail="contact name already exists")
    contact = m_contact.Contact(
        user_id=user.id, friend_id=contact_user.id, alias=in_contact.alias
    )
    return d_contact.create(curs, contact)


@db_connect
def get_all(curs, user: m_user.User) -> Optional[list[m_contact.Contact]]:
    return d_contact.get_all_by_user_id(curs, user.id)
