import mchat.data.user as d_user
from mchat.helper import db_connect


@db_connect
def get_user(curs, id: int):
    return d_user.get(curs, id)


@db_connect
def get_user_by_username(curs, username: str):
    return d_user.get_by_username(curs, username)
