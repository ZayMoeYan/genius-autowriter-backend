from fastapi import FastAPI
from app import database
from .routers import auth, admin, users, contents
import os

app = FastAPI(title="Content Generator API")

@app.on_event("startup")
def on_startup():
    database.Base.metadata.create_all(bind=database.engine)

app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(contents.router)
