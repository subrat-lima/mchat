from typing import Optional

import mchat.helper as db


def add(curs, message):
    statement = """
    INSERT INTO messages
        (data, message_type, sender_id, receiver_id, parent_message_id, expiry_date)
    VALUES
        (:data, :message_type, :sender_id, :receiver_id, :parent_message_id, :expiry_date)
    RETURNING id 
    """
    return db.one(curs, statement, message)


def get(curs, id: int):
    statement = """SELECT 
        m.id, 
        m.expiry_date,
        m.create_date,
        m.message_type,
        m.parent_message_id,
        m.status,
        m.sender_id,
        m.receiver_id,
        m.data,
        users.username as sender_username
    FROM messages m
    JOIN users ON m.sender_id = users.id
    WHERE m.id = ?"""
    return db.one(curs, statement, (id,))


def get_by_chat(curs, chat_users):
    statement = """SELECT 
        m.id, 
        m.expiry_date,
        m.create_date,
        m.message_type,
        m.parent_message_id,
        m.status,
        m.sender_id,
        m.receiver_id,
        m.data,
        users.username as sender_username
    FROM messages m
    JOIN users ON m.sender_id = users.id
    WHERE m.sender_id IN (:user_id, :friend_id) AND m.receiver_id IN (:user_id, :friend_id)
    ORDER BY m.create_date;
    """
    return db.all(curs, statement, chat_users)
