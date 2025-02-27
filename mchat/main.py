from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

import mchat
import mchat.service.websockets as ws
from mchat.routes import auth

app = FastAPI()
app.mount("/static", StaticFiles(directory="mchat/static"), name="static")
app.include_router(auth.router)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws.handler(websocket)


@app.get("/", response_class=HTMLResponse)
async def index():
    with open("mchat/templates/index.html") as f:
        html = f.read()
    return HTMLResponse(html)
