from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from app.configs.mongodb import init_db
from app.errors.error_handler import (
    general_exception_handler,
    http_exception_handler,
    not_found_exception_handler,
    validation_exception_handler,
)
from app.errors.not_found import NotFoundException
from app.middlewares.camel_case_convert_middleware import CamelCaseConvertMiddleware
from app.routes.register_router import register_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()

    yield


app = FastAPI(lifespan=lifespan)

# Add exception handlers
app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
)

# Add camelCase conversion middleware
app.add_middleware(CamelCaseConvertMiddleware)

register_router(app)
