from fastapi import FastAPI

from madr.routers import auth, authors, users

app = FastAPI(
    title="MADR",
    description="⚡Meu Acervo Digital de Romances"
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(authors.router)
