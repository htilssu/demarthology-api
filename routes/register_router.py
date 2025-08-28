from fastapi import FastAPI

from routes import auth


def register_router(app: FastAPI) -> None:
    app.include_router(auth.router)