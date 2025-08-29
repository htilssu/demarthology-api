from fastapi import FastAPI

from app.routes import auth, question, symptom


def register_router(app: FastAPI) -> None:
    app.include_router(auth.router, prefix="/auth")
    app.include_router(symptom.router, prefix="/symptoms")
    app.include_router(question.router, prefix="/questions")
