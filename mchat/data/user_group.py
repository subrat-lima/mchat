from typing import Optional

import mchat.helper as db
from mchat.model import UserGroup, UserGroupIn


def add(curs, UserGroupIn: int) -> bool:
    statement = (
        """INSERT INTO user_groups (user_id, group_id) VALUES(?, ?) RETURNING id"""
    )
    return db.add(curs, statement, (UserGroupIn.user_id, UserGroupIn.group_id))


def get_by_group_and_user(curs, group_id: int, user_id: int) -> UserGroup | None:
    statement = """
    SELECT * FROM user_groups 
    INNER JOIN groups ON groups.id = user_groups.group_id
    WHERE group_id = ? AND user_id = ?;"""
    return db.get(curs, statement, (group_id, user_id), UserGroup)


def get_all_by_id(curs, group_id: int) -> Optional[list[UserGroup]]:
    statement = """SELECT * FROM user_groups WHERE id = ?"""
    return db.get_all(curs, statement, (group_id,), UserGroup)


def get_all_by_user(curs, user_id: int) -> Optional[list[UserGroup]]:
    statement = """
    SELECT * FROM user_groups
    INNER JOIN groups ON groups.id = user_groups.group_id
    WHERE user_id = ?;
    """
    return db.get_all(curs, statement, (user_id,), UserGroup)


def get_all(curs) -> Optional[list[UserGroup]]:
    statement = """
    SELECT * FROM user_groups
    INNER JOIN groups ON groups.id = user_groups.group_id
    """
    return db.get_all(curs, statement, None, UserGroup)
