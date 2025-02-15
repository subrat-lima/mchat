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


def get_all_in_chat(curs, chat_id: int) -> Optional[list[Member]]:
    statement = """SELECT * FROM member WHERE chat_id = ?"""
    curs.execute(statement, (chat_id,))
    rows = curs.fetchall()
    if rows:
        members = [Member(**row) for row in rows]
        return members
    return None


def get_one(curs, chat_id: int, contact_id: int) -> bool:
    statement = """SELECT * FROM member WHERE chat_id = ? AND user_id = ?"""
    curs.execute(statement, (chat_id, contact_id))
    member = curs.fetchone()
    if member:
        return True
    return False
