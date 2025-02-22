from typing import Optional

import mchat.helper as db
from mchat.model import Chat, Message, MessageIn, MessageRecipient, MessageRecipientIn


def add(curs, message_recipient: MessageRecipientIn) -> bool:
    statement = """INSERT INTO message_recipients (recipient_id, recipient_group_id, message_id) VALUES(?, ?, ?) RETURNING id"""
    return db.add(
        curs,
        statement,
        (
            message_recipient.recipient_id,
            message_recipient.recipient_group_id,
            message_recipient.message_id,
        ),
    )


def get_all_received_messages(curs, user_id: int) -> Optional[list[Chat]]:
    statement = """
    SELECT *, username as name, sender_id as recipient_id FROM messages
    INNER JOIN message_recipients ON messages.id = message_recipients.message_id
    INNER JOIN users ON messages.sender_id = users.id
    WHERE recipient_id = ?;
    """
    return db.get_all(curs, statement, (user_id,), Chat)


def get_all_sent_messages(curs, user_id: int) -> Optional[list[Chat]]:
    statement = """
    SELECT username as name, * FROM messages
    INNER JOIN message_recipients ON messages.id = message_recipients.message_id
    INNER JOIN users ON message_recipients.recipient_id = users.id
    WHERE sender_id = ?;
    """
    return db.get_all(curs, statement, (user_id,), Chat)


def get_all(curs) -> Optional[list[MessageRecipient]]:
    statement = """
    SELECT * FROM message_recipients"""
    return db.get_all(curs, statement, None, MessageRecipient)
