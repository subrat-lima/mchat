from typing import Optional

import mchat.data.group as d_group
import mchat.data.message as d_message
import mchat.data.message_recipient as d_message_recipient
import mchat.data.user as d_user
import mchat.data.user_group as d_user_group
from mchat.helper import db_connect
from mchat.model import Chat, Group, Message, MessageRecipient, User, UserGroup


@db_connect
def get_users(curs, user: User) -> Optional[list[User]]:
    return d_user.get_all(curs)


@db_connect
def get_groups(curs, user: User) -> Optional[list[Group]]:
    return d_group.get_all(curs)


@db_connect
def get_user_groups(curs, user: User) -> Optional[list[UserGroup]]:
    return d_user_group.get_all(curs)


@db_connect
def get_messages(curs, user: User) -> Optional[list[Message]]:
    return d_message.get_all(curs)


@db_connect
def get_message_recipients(curs, user: User) -> Optional[list[MessageRecipient]]:
    return d_message_recipient.get_all(curs)
