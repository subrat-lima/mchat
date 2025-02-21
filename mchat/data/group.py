import mchat.helper as db
from mchat.model import Group


def add(curs, user_id: int, name: str) -> bool:
    statement = """INSERT INTO groups (name, owner_id) VALUES(?, ?) RETURNING id"""
    return db.add(curs, statement, (name, user_id))


def get(curs, id: int) -> Group | None:
    statement = """SELECT * FROM groups WHERE id = ?"""
    return db.get(curs, statement, (id,), Group)


def get_by_owner_and_name(curs, user_id: int, group_name: str) -> Group | None:
    statement = """SELECT * FROM groups WHERE owner_id = ? AND name = ?"""
    return db.get(curs, statement, (user_id, group_name), Group)
