from app.repositories.task import TaskRepository
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema


class TaskService:
    """
    Service layer for task-related operations.
    """

    def __init__(self, task_repository: TaskRepository) -> None:
        self.task_repository = task_repository

    async def get_all_tasks(self) -> list[TaskSchema]:
        """
        Retrieve all tasks.
        """
        tasks = await self.task_repository.find_all()
        return [TaskSchema.model_validate(task) for task in tasks]

    async def get_task_by_name(self, name: str) -> TaskSchema:
        """
        Retrieve a specific task by its name.
        """
        task = await self.task_repository.find_one({"name": name})
        return TaskSchema.model_validate(task)

    async def create_task(self, task_data: TaskCreateSchema) -> TaskSchema:
        """
        Create a new task.
        """
        task_dict = task_data.model_dump()
        created_task = await self.task_repository.add_one(task_dict)
        return TaskSchema.model_validate(created_task)

    async def update_task(self, name: str, update_data: TaskUpdateSchema) -> TaskSchema:
        """
        Update an existing task.
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_task = await self.task_repository.update_one(
            {"name": name},
            {"$set": update_dict},
        )
        return TaskSchema.model_validate(updated_task)

    async def delete_task(self, name: str) -> None:
        """
        Delete a task by its name.
        """
        await self.task_repository.delete_one({"name": name})
