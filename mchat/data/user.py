from typing import Optional

from fastapi.security import HTTPBasicCredentials

import mchat.helper as db


def add(curs, user: HTTPBasicCredentials):
    statement = """INSERT INTO users (username, password) VALUES(:username, :password) RETURNING *"""
    return db.one(curs, statement, user.dict())


def get(curs, id: int):
    statement = """SELECT * FROM users WHERE id = :id"""
    return db.one(curs, statement, (id,))


def get_by_username(curs, username: str):
    statement = """SELECT * FROM users WHERE username = ?"""
    return db.one(curs, statement, (username,))


def get_all(curs):
    statement = """SELECT * FROM users"""
    return db.all(curs, statement)
