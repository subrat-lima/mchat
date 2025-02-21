import mchat.helper as db
from mchat.model import User, UserIn


def add(curs, user: UserIn) -> bool:
    statement = """INSERT INTO users (username, password) VALUES(?, ?)"""
    return db.add_one(curs, statement, (user.username, user.password))


def get(curs, id: int) -> User | None:
    statement = """SELECT * FROM users WHERE id = ?"""
    return db.get_one(curs, statement, (id,), User)


def get_by_username(curs, username: str) -> User | None:
    statement = """SELECT * FROM users WHERE username = ?"""
    return db.get_one(curs, statement, (username,), User)


def get_all(curs) -> list[User] | None:
    statement = """SELECT * FROM users"""
    return db.get(curs, statement, None, User)
