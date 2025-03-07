from fastapi import APIRouter, FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.security import HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles

import mchat
import mchat.service.auth as service
import mchat.service.websockets as ws
from mchat.model import Token

app = FastAPI()
app.mount("/static", StaticFiles(directory="mchat/static"), name="static")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws.handler(websocket)


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("mchat/templates/index.html") as f:
        html = f.read()
    return HTMLResponse(html)


@app.post("/register")
async def register(user: HTTPBasicCredentials):
    return service.register(user)


@app.post("/login")
async def login(user: HTTPBasicCredentials):
    return service.login(user)
