import sqlite3

import bcrypt


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def match_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def db_connect(func):
    def _db_connect(*args, **kwargs):
        conn = sqlite3.connect(".instance/mchat.db")
        conn.row_factory = dict_factory
        curs = conn.cursor()
        result = func(curs, *args, **kwargs)
        conn.commit()
        conn.close()
        return result

    return _db_connect


def add(curs, statement, data):
    curs.execute(statement, data)
    row = curs.fetchone()
    return row if row else None


def get(curs, statement, data, cls):
    curs.execute(statement, data)
    row = curs.fetchone()
    if row:
        return cls(**row)
    return None


def get_all(curs, statement, data, cls):
    if data is None:
        curs.execute(statement)
    else:
        curs.execute(statement, data)
    rows = curs.fetchall()
    if rows:
        return [cls(**row) for row in rows]
    return None
