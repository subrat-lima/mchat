from typing import Optional

import mchat.helper as db
from mchat.model import Message, MessageIn


def add(curs, user_id: int, message: MessageIn) -> bool:
    statement = """INSERT INTO messages (sender_id, message, category, parent_message_id) VALUES(?, ?, ?, ?) RETURNING id"""
    print("message:", message)
    print("user_id:", user_id)
    return db.add(
        curs,
        statement,
        (
            user_id,
            message.message,
            message.category,
            message.parent_message_id,
        ),
    )


def get_by_group_and_user(curs, group_id: int, user_id: int) -> Message | None:
    # TODO: change function
    statement = """
    SELECT * FROM user_groups 
    INNER JOIN groups ON groups.id = user_groups.group_id
    WHERE group_id = ? AND user_id = ?;"""
    return db.get(curs, statement, (group_id, user_id), Message)


def get_all(curs) -> Optional[list[Message]]:
    statement = """SELECT * FROM messages"""
    return db.get_all(curs, statement, None, Message)
