import uvicorn
from fastapi import FastAPI

import mchat
from mchat.web import auth, contact, user

app = FastAPI()
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(contact.router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
