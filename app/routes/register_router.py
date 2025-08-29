from fastapi import FastAPI

from app.routes import auth, symptom


def register_router(app: FastAPI) -> None:
    app.include_router(auth.router, prefix="/auth")
    app.include_router(symptom.router, prefix="/symptoms")
