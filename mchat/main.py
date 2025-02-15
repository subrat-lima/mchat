import uvicorn
from fastapi import FastAPI

import mchat
from mchat.web import auth, chat, contact, user

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(contact.router)
app.include_router(chat.router)


def main():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
