from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.db.database import db_client
from app.middlewares.exception_middleware import ExceptionMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.core.logger_setup import get_logger
from app.api.v1 import router as router_v1

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    logger.info("Starting up the application...")
    await db_client.connect()
    logger.info("MongoDB client initialized and connected.")
    yield
    await db_client.close()
    logger.info("MongoDB client closed.")
    logger.info("Shutting down the application...")


app = FastAPI(
    title="Code Runner API",
    description="API for running user-submitted Python code against predefined tasks.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "melchikov04@mail.ru",
    },
    lifespan=lifespan,
)


origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)
app.add_middleware(ExceptionMiddleware)

app.include_router(router=router_v1, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
