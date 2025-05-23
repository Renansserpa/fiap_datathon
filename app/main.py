
from fastapi import FastAPI

from . import auth, users

app = FastAPI()
app.get('/')

app.include_router(users.router)
app.include_router(auth.router)