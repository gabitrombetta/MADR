from fastapi import FastAPI

from madr.routers import auth, novelists, users

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(novelists.router)
