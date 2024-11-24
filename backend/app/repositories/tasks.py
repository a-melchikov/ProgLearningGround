import asyncio
from typing import Any

from pymongo import errors

from app.errors.task_errors import TaskNotFound, DatabaseConnectionError
from app.database import AsyncMongoDBClient
from app.logger_setup import get_logger

logger = get_logger(__name__)


class TaskRepository:
    """
    Repository class for managing tasks.
    """

    def __init__(
        self,
        db_client: AsyncMongoDBClient,
        collection_name: str = "tasks",
    ) -> None:
        self.db_client = db_client
        self.collection_name = collection_name

    async def get_task(
        self,
        task_name: str,
    ) -> dict[str, Any]:
        """
        Fetches a task by its name.
        """
        try:
            collection = await self.db_client.get_collection(self.collection_name)
            task_data = await collection.find_one("name", task_name)
            if not task_data:
                logger.info(f"Task '{task_name}' not found.")
                raise TaskNotFound(task_name=task_name)
            logger.info(f"Fetched task '{task_name}'")
            return task_data
        except TaskNotFound as e:
            logger.info(f"Task '{task_name}' not found.")
            raise e
        except errors.PyMongoError as e:
            logger.error(f"Error while fetching task '{task_name}': {str(e)}")
            raise DatabaseConnectionError(
                f"Error while accessing database: {str(e)}"
            ) from e

    async def get_tasks(
        self,
        filter_query: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        List all tasks or tasks matching a filter.
        """
        try:
            collection = await self.db_client.get_collection(self.collection_name)
            cursor = collection.find(filter_query or {})
            tasks = await cursor.to_list(length=None)
            logger.info(f"Fetched {len(tasks)} task(s)")
            return tasks
        except errors.PyMongoError as e:
            logger.error(f"Error while listing tasks: {str(e)}")
            raise DatabaseConnectionError(
                f"Error while fetching tasks: {str(e)}"
            ) from e

    async def create_task(
        self,
        task_data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Create a new task.
        """
        try:
            collection = await self.db_client.get_collection(self.collection_name)
            result = await collection.insert_one(task_data)
            task_data["_id"] = str(result.inserted_id)
            logger.info(f"Created task with name '{task_data.get('name')}'")
            return task_data
        except errors.PyMongoError as e:
            logger.error(f"Database error while creating task: {str(e)}")
            raise DatabaseConnectionError(
                f"Error while inserting task data: {str(e)}"
            ) from e

    async def update_task(
        self,
        task_name: str,
        update_data: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Update an existing task by its name.
        """
        try:
            collection = await self.db_client.get_collection(self.collection_name)
            result = await collection.update_one(
                {"name": task_name}, {"$set": update_data}
            )
            if result.matched_count == 0:
                logger.info(f"Task '{task_name}' not found for update.")
                raise TaskNotFound(task_name=task_name)
            updated_task = await collection.find_one({"name": task_name})
            logger.info(f"Updated task '{task_name}'")
            return updated_task
        except TaskNotFound as e:
            raise e
        except errors.PyMongoError as e:
            logger.error(f"Error while updating task '{task_name}': {str(e)}")
            raise DatabaseConnectionError(
                f"Error while updating task data: {str(e)}"
            ) from e

    async def delete_task(
        self,
        task_name: str,
    ) -> None:
        """
        Delete a task by its name.
        """
        try:
            collection = await self.db_client.get_collection(self.collection_name)
            result = await collection.delete_one({"name": task_name})
            if result.deleted_count == 0:
                logger.info(f"Task '{task_name}' not found for deletion.")
                raise TaskNotFound(task_name=task_name)
            logger.info(f"Deleted task '{task_name}'")
        except TaskNotFound as e:
            raise e
        except errors.PyMongoError as e:
            logger.error(f"Error while deleting task '{task_name}': {str(e)}")
            raise DatabaseConnectionError(
                f"Error while deleting task data: {str(e)}"
            ) from e


async def main() -> None:
    client = AsyncMongoDBClient()
    await client.connect()
    task_repository = TaskRepository(client)
    # task_data = {
    #     "name": "sum_with_inversion",
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
        # created_task = await task_repository.create_task(task_data)
        # logger.info(f"Task '{created_task['name']}' successfully created.")
        all_tasks = await task_repository.get_tasks()
        logger.info(f"All tasks '{all_tasks}'")
    except DatabaseConnectionError as e:
        logger.error(f"Error while creating task: {str(e)}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
