from fastapi import WebSocket, WebSocketDisconnect

import mchat.service.auth as s_auth
import mchat.service.chat as s_chat
import mchat.service.contact as s_contact
import mchat.service.message as s_message
import mchat.service.user as s_user


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, username: str, websocket: WebSocket):
        if self.active_connections.get(username, None) is None:
            self.active_connections[username] = []
        self.active_connections[username].append(websocket)

    async def disconnect(self, username: str, websocket: WebSocket):
        self.active_connections[username].remove(websocket)

    async def send_message_to_users(self, message: dict, usernames: list[str]):
        for username in usernames:
            for connection in self.active_connections.get(username, []):
                await connection.send_json(message)


manager = ConnectionManager()


async def handleRequest(user, websocket, data):
    action = data["action"]
    if action == "get-chat-list":
        chats = s_chat.get_chats_by_user(user["id"])
        resp = {"action": action, "from": data["from"], "chats": chats}
        await websocket.send_json(resp)
    elif action == "open-chat":
        messages = s_message.get_by_chat(user["id"], data["receiver_id"])
        resp = {
            "action": action,
            "from": data["from"],
            "chat": {"id": data["receiver_id"], "name": data["receiver_name"]},
            "messages": messages,
        }
        await websocket.send_json(resp)
    elif action == "send-message":
        message = data["message"]
        message["sender_id"] = user["id"]
        db_resp = s_message.add(message)
        db_message = s_message.get(db_resp["id"])
        receiver = s_user.get(message["receiver_id"])
        resp = {"action": action, "message": db_message}
        await manager.send_message_to_users(resp, [receiver["username"]])
        resp["from"] = data["from"]
        await websocket.send_json(resp)
    elif action == "add-chat":
        receiver = s_user.get_by_username(data["username"])
        if receiver is None:
            error_resp = {
                "action": action,
                "from": data["from"],
                "status": "failed",
                "error": "user not found",
            }
            await websocket.send_json(error_resp)
            return
        messages = s_message.get_by_chat(user["id"], receiver["id"])
        resp = {
            "action": action,
            "from": data["from"],
            "status": "ok",
            "chat": {"id": receiver["id"], "name": receiver["username"]},
            "messages": messages,
        }
        await websocket.send_json(resp)
    elif action == "get-contacts":
        contacts = s_contact.get_by_user(user["id"])
        resp = {
            "action": action,
            "from": data["from"],
            "status": "ok",
            "contacts": contacts,
        }
        await websocket.send_json(resp)


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
                "user": {"username": user["username"], "id": user["id"]},
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
        await manager.disconnect(user["username"], websocket)
