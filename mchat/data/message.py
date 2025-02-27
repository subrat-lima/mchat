from typing import Optional

import mchat.helper as db


def add(curs, message):
    statement = """
    INSERT INTO messages
        (data, message_type, sender_id, receiver_id, parent_message_id, expiry_date)
    VALUES
        (:data, :message_type, :sender_id, :receiver_id, :parent_message_id, :expiry_date)
    RETURNING *"""
    return db.one(curs, statement, message)


def get(curs, id: int):
    statement = """SELECT * FROM messages WHERE id = ?"""
    return db.one(curs, statement, (id,))


def get_by_chat(curs, chat_users):
    statement = """SELECT * FROM messages WHERE sender_id IN (:user_id, :friend_id) AND receiver_id IN (:user_id, :friend_id)"""
    return db.all(curs, statement, chat_users)
