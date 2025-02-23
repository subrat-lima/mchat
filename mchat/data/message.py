from typing import Optional

import mchat.helper as db
from mchat.model import GroupMessageOut, Message, MessageIn, MessageOut


def add(curs, user_id: int, message: MessageIn) -> bool:
    statement = """INSERT INTO messages (sender_id, message, category, parent_message_id) VALUES(?, ?, ?, ?) RETURNING id"""
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


def get_all_by_direct_chat_id(
    curs, user_id: int, contact_id: int
) -> Optional[list[MessageOut]]:
    statement = """
    SELECT
        messages.id as id, 
        message,
        sender_id,
        messages.create_date as create_date,
        username as sender_name
    FROM
        messages
    INNER JOIN
        message_recipients ON
        message_recipients.message_id = messages.id
    INNER JOIN
        users ON
        users.id = messages.sender_id
    WHERE
        (messages.sender_id = ? AND message_recipients.recipient_id = ?)
    OR
        (messages.sender_id = ? AND message_recipients.recipient_id = ?)
    """
    return db.get_all(
        curs, statement, (user_id, contact_id, contact_id, user_id), MessageOut
    )


def get_all_by_group_chat_id(curs, chat_id: int) -> Optional[list[GroupMessageOut]]:
    statement = """
    SELECT
        messages.id as id,
        message,
        sender_id,
        recipient_group_id as group_id,
        messages.create_date as create_date,
        username as sender_name
    FROM
        messages
    INNER JOIN
        message_recipients ON
        message_recipients.message_id = messages.id
    INNER JOIN
        users ON
        users.id = messages.sender_id
    WHERE
        message_recipients.recipient_group_id = ?
    """
    return db.get_all(curs, statement, (chat_id,), GroupMessageOut)
