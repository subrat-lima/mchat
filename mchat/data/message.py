from datetime import datetime
from typing import Optional

from mchat.model.member import Member
from mchat.model.message import Message


def create(curs, message: Message) -> int:
    statement = """INSERT INTO message (chat_id, user_id, content_type_id, content) VALUES(?, ?, ?, ?) RETURNING *"""
    curs.execute(
        statement,
        (
            message.chat_id,
            message.user_id,
            message.content_type_id,
            message.content,
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


def get_all_in_chat(curs, chat_id: int) -> Optional[list[Message]]:
    statement = """SELECT * FROM message WHERE chat_id = ?"""
    curs.execute(statement, (chat_id,))
    rows = curs.fetchall()
    if rows:
        messages = [Message(**row) for row in rows]
        return messages
    return None


def get_one(curs, chat_id: int, contact_id: int) -> bool:
    statement = """SELECT * FROM member WHERE chat_id = ? AND user_id = ?"""
    curs.execute(statement, (chat_id, contact_id))
    member = curs.fetchone()
    if member:
        return True
    return False
