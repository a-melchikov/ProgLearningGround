from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.logger_setup import get_logger

logger = get_logger(__name__)

BASE_DIR = Path(__file__).parent.parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

logger.info(f"Base directory: {BASE_DIR}")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    MONGO_DB_USER: str
    MONGO_DB_PASSWORD: str
    MONGO_DB_HOST: str
    MONGO_DB_PORT: int
    MONG0_DB_NAME: str

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        logger.info("Settings initialized successfully")
        logger.info(self.model_dump())

    def get_mongo_db_url(self) -> str:
        return f"mongodb://{self.MONGO_DB_USER}:{self.MONGO_DB_PASSWORD}@{self.MONGO_DB_HOST}:{self.MONGO_DB_PORT}/"


settings = Settings()

if __name__ == "__main__":
    print(ENV_FILE_PATH)
    print(settings.model_dump())
    print(settings.get_mongo_db_url())
