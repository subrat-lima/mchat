import mchat.data.chat as d_chat
from mchat.helper import db_connect


@db_connect
def get_chats_by_user(curs, user_id):
    return d_chat.get_by_user(curs, user_id)
