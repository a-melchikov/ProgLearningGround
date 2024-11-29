from app.db.database import AsyncMongoDBClient
from app.repositories.task import TaskRepository
from app.services.task import TaskService
from app.core.logger_setup import get_logger

logger = get_logger(__name__)


async def get_task_service() -> TaskService:
    client = AsyncMongoDBClient()
    await client.connect()
    logger.info("MongoDB client initialized and connected.")
    try:
        repository = TaskRepository(client)
        return TaskService(repository)
    finally:
        await client.close()
        logger.info("MongoDB client closed.")
