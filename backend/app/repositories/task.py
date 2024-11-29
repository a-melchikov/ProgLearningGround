import asyncio

from app.errors.task_errors import TaskNotFound, TaskDatabaseConnectionError
from app.db.database import AsyncMongoDBClient
from app.core.logger_setup import get_logger
from app.utils.repository import MongoDBRepository

logger = get_logger(__name__)


class TaskRepository(MongoDBRepository):
    """
    Repository class for managing tasks.
    """

    def __init__(
        self,
        db_client: AsyncMongoDBClient,
        collection_name: str = "tasks",
    ) -> None:
        super().__init__(
            db_client=db_client,
            collection_name=collection_name,
            log_name="task",
            not_found_error=TaskNotFound,
            database_connection_error=TaskDatabaseConnectionError,
        )


async def main() -> None:
    client = AsyncMongoDBClient()
    await client.connect()
    task_repository = TaskRepository(client)
    # task_data = {
    #     "name": "sum_with_inversion1",
    #     "description": "Дано двузначное число. Нужно его развернуть, и сложить результат с исходным числом.",
    #     "input": "Целое число на отрезке 10..99.",
    #     "output": "Выражение вида: (исходное число) + (развернутое число) = (сумма).",
    #     "examples": [
    #         {"input": "82", "output": "82 + 28 = 110"},
    #         {"input": "27", "output": "27 + 72 = 99"},
    #     ],
    #     "test_cases": [
    #         {"input": "34", "expected_output": "34 + 43 = 77"},
    #         {"input": "45", "expected_output": "45 + 54 = 99"},
    #         {"input": "78", "expected_output": "78 + 87 = 165"},
    #         {"input": "12", "expected_output": "12 + 21 = 33"},
    #     ],
    # }

    try:
        # created_task = await task_repository.add_one(task_data)
        # logger.info(f"Task '{created_task['name']}' successfully created.")
        # one_task = await task_repository.find_one({"name": "sum_with_inversion32"})
        all_tasks = await task_repository.find_all()
        logger.info(f"All tasks '{all_tasks}'")
    except TaskDatabaseConnectionError as e:
        logger.error(f"Error while creating task: {str(e)}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
