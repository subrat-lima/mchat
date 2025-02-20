import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import mchat
from mchat.web import auth, chat, contact, member, message, user

app = FastAPI()
app.mount("/static", StaticFiles(directory="mchat/static"), name="static")
templates = Jinja2Templates(directory="mchat/templates")

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(contact.router)
app.include_router(chat.router)
app.include_router(member.router)
app.include_router(message.router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


def main():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
