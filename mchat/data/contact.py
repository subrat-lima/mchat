from typing import Optional

from mchat.model.contact import Contact


def create(curs, contact: Contact) -> bool:
    statement = """INSERT INTO contact (user_id, friend_id, alias) VALUES(?, ?, ?)"""
    curs.execute(statement, (contact.user_id, contact.friend_id, contact.alias))
    return True


def get_one(curs, user_id: id, friend_id: id) -> Optional[Contact]:
    statement = """SELECT * FROM contact WHERE user_id = ? AND friend_id = ?"""
    curs.execute(statement, (user_id, friend_id))
    contact = curs.fetchone()
    if contact:
        return Contact(**contact)
    return None


def get_one_by_alias(curs, user_id: id, alias: str) -> Optional[Contact]:
    statement = """SELECT * FROM contact WHERE user_id = ? AND alias = ?"""
    curs.execute(statement, (user_id, alias))
    contact = curs.fetchone()
    if contact:
        return Contact(**contact)
    return None


def get_all_by_user_id(curs, user_id: int) -> Optional[list[Contact]]:
    statement = """SELECT * FROM contact WHERE user_id = ?"""
    curs.execute(statement, (user_id,))
    rows = curs.fetchall()
    if rows:
        contacts = [Contact(**row) for row in rows]
        return contacts
    return None
