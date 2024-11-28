from app.database import AsyncMongoDBClient
from app.repositories.task import TaskRepository
from app.services.task import TaskService


async def get_task_service() -> TaskService:
    client = AsyncMongoDBClient()
    await client.connect()
    task_repository = TaskRepository(client)
    return TaskService(task_repository)
