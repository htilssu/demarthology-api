from fastapi import FastAPI

from app.routes import auth


def register_router(app: FastAPI) -> None:
    app.include_router(auth.router)