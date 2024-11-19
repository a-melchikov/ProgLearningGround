from fastapi import FastAPI
from logger_setup import get_logger

logger = get_logger(__name__)
app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    logger.info("Получен запрос на главную страницу")
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str) -> dict[str, str]:
    return {"message": f"Hello {name}"}
