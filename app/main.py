from fastapi import FastAPI
import auth, users, webscrapper
import os

app = FastAPI()
app.get('/')

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(webscrapper.router)