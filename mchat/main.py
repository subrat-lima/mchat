from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import mchat
from mchat.routes import admin, auth, chat
from mchat.service.websockets import websocket_handler

app = FastAPI()
app.mount("/static", StaticFiles(directory="mchat/static"), name="static")
templates = Jinja2Templates(directory="mchat/templates")

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(chat.router)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_handler(websocket)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")
