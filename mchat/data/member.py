from datetime import datetime
from typing import Optional

from mchat.model.member import Member


def create(curs, member: Member) -> int:
    statement = """INSERT INTO member (chat_id, user_id, role_id, joined_at, left_at) VALUES(?, ?, ?, ?, ?) RETURNING *"""
    curs.execute(
        statement,
        (
            member.chat_id,
            member.user_id,
            member.role_id,
            member.joined_at,
            member.left_at,
        ),
    )
    row = curs.fetchone()
    return row


def get_direct_id(curs, user_id: int, contact_id: int) -> Optional[int]:
    statement = """SELECT * FROM member WHERE (chat_id = ? OR chat_id = ?) AND chat_id in (SELECT id FROM chat WHERE chat_type_id = 1)"""
    curs.execute(statement, (user_id, contact_id))
    member = curs.fetchone()
    if member:
        return Member(**member).chat_id
    return None
