from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.configs.mongodb import init_db
from app.middleware.auth_middleware import AuthMiddleware
from app.routes.register_router import register_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]
)

app.add_middleware(AuthMiddleware)

register_router(app)
