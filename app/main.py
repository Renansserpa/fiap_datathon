from fastapi import FastAPI
import auth, users, webscrapper

app = FastAPI()
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(webscrapper.router)