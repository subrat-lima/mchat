from typing import Optional

from mchat.model.chat import Chat, ChatOut, DirectChatOut


def create(curs, chat_type_id: int) -> int:
    statement = """INSERT INTO chat (chat_type_id) VALUES(?) RETURNING id"""
    curs.execute(statement, (chat_type_id,))
    row = curs.fetchone()
    value = row["id"] if row else None
    return value


def get_one(curs, id: int) -> Optional[Chat]:
    statement = """SELECT * FROM chat WHERE id = ?"""
    curs.execute(statement, (id,))
    chat = curs.fetchone()
    if chat:
        return Chat(**chat)
    return None


def get_all_by_user_id(curs, user_id: int) -> Optional[list[Chat]]:
    statement = """SELECT 
        chat.id as id,
        chat.chat_type_id as type
    FROM member
    INNER JOIN chat on member.chat_id = chat.id
    WHERE member.user_id = ?"""
    curs.execute(statement, (user_id,))
    rows = curs.fetchall()
    print("rows: ", rows)
    if rows:
        chats = [ChatOut(**row) for row in rows]
        return chats
    return None


def create_direct_chat(curs, user_id: int, friend_id: int) -> bool:
    statement = """INSERT INTO direct_chat(user_1_id, user_2_id) VALUES(?)"""
    user_1_id, user_2_id = user_id, friend_id
    if user_id > friend_id:
        user_1_id, user_2_id = friend_id, user_id
    curs.execute(statement, (user_1_id, user_2_id))
    return True


def get_direct_chat(curs, user_id: int, friend_id: int) -> Optional[DirectChatOut]:
    statement_1 = """
    SELECT
        direct_chat.id as id,
        contact.alias as username
    FROM direct_chat
    INNER JOIN user ON
        direct_chat.user_1_id = contact.user_id AND
        direct_chat.user_2_id = contact.friend_id 
    WHERE
        direct_chat.user_1_id = ? AND
        direct_chat.user_2_id = ?
    """

    statement_2 = """
    SELECT
        direct_chat.id as id,
        contact.alias as username
    FROM direct_chat
    INNER JOIN user ON
        direct_chat.user_2_id = contact.user_id AND
        direct_chat.user_1_id = contact.friend_id
    WHERE
        direct_chat.user_1_id = ? AND
        direct_chat.user_2_id = ?
    """

    user_1_id, user_2_id, statement = user_id, friend_id, statement_1
    if user_id > friend_id:
        user_1_id, user_2_id, statement = friend_id, user_id, statement_2
    statement = """
    SELECT
        direct_chat.id as id,
        user.username as username 
    FROM direct_chat
    INNER JOIN user on
        direct_chat.user_1_id = user.id
    """
    curs.execute(statement, (user_1_id, user_2_id))
    chat = curs.fetchone()
    if chat:
        return DirectChatOut(**chat)
    return None


def get_all_direct_chat(curs, user_id: int) -> Optional[list[DirectChatOut]]:
    statement = """SELECT """
    return None
