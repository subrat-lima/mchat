import mchat.helper as db
from mchat.model import UserGroup, UserGroupIn


def add(curs, UserGroupIn: int) -> bool:
    statement = (
        """INSERT INTO user_groups (user_id, group_id) VALUES(?, ?) RETURNING id"""
    )
    return db.add(curs, statement, (UserGroupIn.user_id, UserGroupIn.group_id))


def get_by_group_and_user(curs, group_id: int, user_id: int) -> UserGroup | None:
    statement = """SELECT * FROM user_groups WHERE group_id = ? AND user_id = ?"""
    return db.get(curs, statement, (group_id, user_id), UserGroup)
