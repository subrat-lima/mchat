from typing import Optional

from fastapi import HTTPException

import mchat.data.group as d_group
import mchat.data.message as d_message
import mchat.data.message_recipient as d_message_recipient
import mchat.data.user as d_user
import mchat.data.user_group as d_user_group
from mchat.helper import db_connect
from mchat.model import (
    Chat,
    GroupIn,
    Message,
    MessageIn,
    MessageOut,
    MessageRecipientIn,
    SuccessHandler,
    User,
    UserGroupIn,
)


@db_connect
def get_user(curs, id: int):
    return d_user.get(curs, id)


@db_connect
def get_user_by_username(curs, username: str):
    return d_user.get_by_username(curs, username)


@db_connect
def add_group(curs, user: User, in_group: GroupIn):
    db_group = d_group.get_by_owner_and_name(curs, user.id, in_group.name)
    if db_group:
        raise HTTPException(status_code=400, detail="group already exists")
    db_group = d_group.add(curs, user.id, in_group.name)
    user_group = UserGroupIn(user_id=user.id, group_id=db_group["id"], role=2)
    d_user_group.add(curs, user_group)
    return SuccessHandler(detail="group created successfully", data=db_group)


@db_connect
def add_user_group(curs, user: User, in_user_group: UserGroupIn):
    db_group = d_group.get(curs, in_user_group.group_id)
    if not db_group:
        raise HTTPException(status_code=400, detail="group does not exists")
    db_user_group = d_user_group.get_by_group_and_user(
        curs, db_group.id, in_user_group.user_id
    )
    if db_user_group:
        raise HTTPException(status_code=400, detail="user in group already exists")
    if db_group.owner_id != user.id:
        db_current_user_group = d_user_group.get_by_group_and_user(
            curs, db_group.id, user.id
        )
        if db_current_user_group["role"] == 0:
            raise HTTPException(status_code=403, detail="unauthorized access")
    d_user_group.add(curs, in_user_group)
    return SuccessHandler(detail="user in group add successfully")


@db_connect
def add_message(curs, user: User, in_message: MessageIn):
    db_message = d_message.add(curs, user.id, in_message)
    recipient = MessageRecipientIn(
        recipient_id=in_message.recipient_id,
        recipient_group_id=in_message.recipient_group_id,
        message_id=db_message["id"],
    )
    d_message_recipient.add(curs, recipient)
    return {"id": db_message["id"]}


@db_connect
def get_chats(curs, user: User) -> Optional[list[Chat]]:
    db_user_groups = d_user_group.get_all_by_user(curs, user.id)
    chats = []
    if db_user_groups:
        for group in db_user_groups:
            chat = Chat(recipient_id=None, recipient_group_id=group.id, name=group.name)
            chats.append(chat)
    db_received_messages = d_message_recipient.get_all_received_messages(curs, user.id)
    if db_received_messages:
        for message in db_received_messages:
            chats.append(message)
    db_sent_messages = d_message_recipient.get_all_sent_messages(curs, user.id)
    if db_sent_messages:
        for message in db_sent_messages:
            chats.append(message)
    chats.sort(reverse=True)
    return set(chats)


@db_connect
def get_chat_name(curs, user_id, receiver_id, chat_type):
    if chat_type == "group":
        name = d_group.get(curs, receiver_id).name
    else:
        name = d_user.get(curs, receiver_id).username
    return name


@db_connect
def get_messages(
    curs, user: User, chat_type: str, chat_id: int
) -> Optional[list[MessageOut]]:
    messages = []
    if chat_type == "direct":
        db_messages = d_message.get_all_by_direct_chat_id(curs, user.id, chat_id)
    elif chat_type == "group":
        db_messages = d_message.get_all_by_group_chat_id(curs, chat_id)
    if db_messages:
        for message in db_messages:
            messages.append(message)
    messages.sort()
    return messages


@db_connect
def get_message(curs, message_id):
    return d_message.get(curs, message_id)
