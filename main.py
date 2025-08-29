from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.configs.mongodb import init_db
from app.middlewares.camel_case_convert_middleware import CamelCaseConvertMiddleware
from app.routes.register_router import register_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], )

# Add camelCase conversion middleware
app.add_middleware(CamelCaseConvertMiddleware)

register_router(app)
