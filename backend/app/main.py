from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.middlewares.exception_middleware import ExceptionMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from app.core.logger_setup import get_logger
from app.api.v1 import router as router_v1

logger = get_logger(__name__)

app = FastAPI(
    title="Code Runner API",
    description="API for running user-submitted Python code against predefined tasks.",
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "melchikov04@mail.ru",
    },
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
        "main_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
