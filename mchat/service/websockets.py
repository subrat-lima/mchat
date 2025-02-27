from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect

import mchat.service.auth as s_auth
import mchat.service.chat as s_chat
from mchat.helper import db_connect
from mchat.model import MessageIn


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, username: str, websocket: WebSocket):
        if self.active_connections.get(username, None) is None:
            self.active_connections[username] = []
        self.active_connections[username].append(websocket)

    async def disconnect(self, username: str, websocket: WebSocket):
        self.active_connections[username].remove(websocket)

    async def send_message_to_chat(
        self, message: dict, usernames: list[str], websocket: WebSocket
    ):
        for username in usernames:
            for connection in self.active_connections.get(username, []):
                await connection.send_json(message)


manager = ConnectionManager()


async def handleRequest(user, websocket, data):
    action = data["action"]
    if action == "get-chat-list":
        chats = s_chat.get_chats_by_user(user["id"])
        print("chats: ", chats)
        resp = {"action": action, "from": data["from"], "chats": chats}
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
    elif action == "add-chat":
        print("data:", data)
        recipient_username = data["data"]["username"]
        print("recipient_username: ", recipient_username)
        recipient = s_chat.get_user_by_username(recipient_username)
        await websocket.send_json(
            {
                "action": action,
                "from": data["from"],
                "status": "ok",
                "data": {
                    "receiver_id": recipient.id,
                    "name": recipient.username,
                    "type": "direct",
                },
            }
        )


async def handler(websocket: WebSocket):
    await websocket.accept()
    try:
        j_data = await websocket.receive_json()
        token = j_data["data"]["token"]
        user = s_auth.get_user_from_token(token)
        await websocket.send_json(
            {
                "action": "token",
                "from": j_data["data"]["from"],
                "status": "ok",
                "data": {"username": user["username"], "id": user["id"]},
            }
        )
    except Exception:
        await websocket.send_json(
            {"action": "token", "status": "failed", "error": "invalid token"}
        )
        await websocket.close()
        return

    await manager.connect(user["username"], websocket)
    try:
        while True:
            j_data = await websocket.receive_json()
            await handleRequest(user, websocket, j_data["data"])
    except WebSocketDisconnect:
        manager.disconnect(user["username"], websocket)
