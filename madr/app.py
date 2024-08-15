from fastapi import FastAPI

from madr.routers import users

app = FastAPI()

app.include_router(users.router)
