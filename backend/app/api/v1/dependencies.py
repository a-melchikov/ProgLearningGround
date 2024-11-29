from app.db.database import db_client
from app.repositories.task import TaskRepository
from app.services.task import TaskService
from app.core.logger_setup import get_logger

logger = get_logger(__name__)


async def get_task_service() -> TaskService:
    repository = TaskRepository(db_client)
    service = TaskService(repository)
    return service
