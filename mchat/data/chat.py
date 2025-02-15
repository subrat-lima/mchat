from typing import Optional

from mchat.model.chat import Chat


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
    statement = """SELECT * FROM chat WHERE id = (SELECT chat_id FROM member WHERE chat_id = ?)"""
    curs.execute(statement, (user_id,))
    rows = curs.fetchall()
    if rows:
        chats = [Chat(**row) for row in rows]
        return chats
    return None
