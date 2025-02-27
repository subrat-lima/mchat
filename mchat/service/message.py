import mchat.data.message as d_message
from mchat.helper import db_connect


@db_connect
def add_message(curs, message):
    return d_message.add(curs, message)


@db_connect
def get(curs, id):
    return d_message.get(curs, id)


@db_connect
def get_by_chat(curs, user_id, friend_id):
    return d_message.get_by_chat({"user_id": user_id, "friend_id": friend_id})
