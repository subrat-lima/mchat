from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect

import mchat.data.message as d_message
import mchat.data.message_recipient as d_message_recipient
import mchat.data.user as d_user
from mchat.helper import db_connect
from mchat.model import MessageIn
from mchat.service.auth import get_user
from mchat.service.chat import add_message


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
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
                if connection != websocket:
                    await connection.send_json(message)


manager = ConnectionManager()


@db_connect
def get_user_direct(curs, id: int):
    return d_user.get(curs, id)


@db_connect
def get_message(curs, id: int):
    return d_message.get(curs, id)


async def send_message_to_chat(username, websocket, data):
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


async def websocket_handler(websocket: WebSocket, username: str):
    await manager.connect(username, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type", None) == "send_message":
                await send_message_to_chat(username, websocket, data)
    except WebSocketDisconnect:
        manager.disconnect(username, websocket)
