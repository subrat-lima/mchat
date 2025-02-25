from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect

import mchat.data.message as d_message
import mchat.data.message_recipient as d_message_recipient
import mchat.data.user as d_user
import mchat.service.chat as s_chat
from mchat.helper import db_connect
from mchat.model import MessageIn
from mchat.service.auth import get_user
from mchat.service.chat import add_message


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, username: str, websocket: WebSocket):
        if not self.active_connections:
            self.active_connections = {}
        if self.active_connections.get(username, None) is None:
            self.active_connections[username] = []
        self.active_connections[username].append(websocket)

    def disconnect(self, username: str, websocket: WebSocket):
        self.active_connections[username].remove(websocket)

    async def send_personal_message(
        self, message: str, username: str, websocket: WebSocket
    ):
        for connection in self.active_connections[username]:
            await connection.send_text(message)

    async def send_message_to_chat(
        self, message: dict, usernames: list[str], websocket: WebSocket
    ):
        for username in usernames:
            for connection in self.active_connections.get(username, []):
                await connection.send_json(message)


manager = ConnectionManager()


@db_connect
def get_user_direct(curs, id: int):
    return d_user.get(curs, id)


@db_connect
def get_message(curs, id: int):
    return d_message.get(curs, id)


async def send_message_to_chat(websocket, data):
    user = get_user(data["token"])
    recipient = get_user_direct(data["recipient_id"])
    in_message = MessageIn(**data)
    status = add_message(user, in_message)
    usernames = [username, recipient.username]
    text = {
        "id": status.data["id"],
        "temp_id": data["temp_id"],
        "message": "message added",
    }
    text = get_message(status.data["id"]).dict()
    text["action"] = "add_message"
    await manager.send_message_to_chat(text, usernames, websocket)


async def handleRequest(user, websocket, data):
    action = data["action"]
    if action == "get-chat-list":
        chats = s_chat.get_chats(user)
        chats = [chat.dict() for chat in chats]
        resp = {"action": action, "from": data["from"], "data": chats}
        await websocket.send_json(resp)
    elif action == "open-chat":
        messages = s_chat.get_messages(user, data["type"], data["receiver_id"])
        messages = [message.dict() for message in messages]
        resp = {"action": action, "from": data["from"], "data": messages}
        chat_name = s_chat.get_chat_name(user.id, data["receiver_id"], data["type"])
        resp["chat"] = {
            "current_user": user.username,
            "receiver_id": data["receiver_id"],
            "type": data["type"],
            "name": chat_name,
        }
        await websocket.send_json(resp)
    elif action == "send-message":
        category = 0 if data["type"] == "direct" else 1
        if data["type"] == "direct":
            recipient_id = data["receiver_id"]
            recipient_group_id = None
        else:
            recipient_group_id = data["receiver_id"]
            recipient_id = None
        parent_id = None if data["parent_id"] == "" else int(data["parent_id"])
        in_message = MessageIn(
            message=data["message"],
            category=category,
            parent_message_id=parent_id,
            recipient_id=recipient_id,
            recipient_group_id=recipient_group_id,
        )
        msg_id = s_chat.add_message(user, in_message)
        message = s_chat.get_message(msg_id["id"])
        resp = {
            "action": action,
            "from": data["from"],
            "data": message.dict(),
            "current_user": user.username,
        }
        recipient = s_chat.get_user(recipient_id)
        recipient_resp = {
            "action": action,
            "data": message.dict(),
            "current_user": recipient.username,
        }
        await websocket.send_json(resp)
        await manager.send_message_to_chat(
            recipient_resp, [recipient.username], websocket
        )


async def websocket_handler(websocket: WebSocket):
    await websocket.accept()
    try:
        j_data = await websocket.receive_json()
        token = j_data["data"]["token"]
        user = get_user(token)
        await websocket.send_json(
            {"action": "token", "from": j_data["data"]["from"], "data": "successful"}
        )
    except Exception:
        await websocket.close()
        return

    await manager.connect(user.username, websocket)
    try:
        while True:
            j_data = await websocket.receive_json()
            data = j_data["data"]
            await handleRequest(user, websocket, data)
    except WebSocketDisconnect:
        manager.disconnect(user.username, websocket)
