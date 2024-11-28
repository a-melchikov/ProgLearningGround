from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status

from app.api.v1.dependencies import get_task_service
from app.errors.task_errors import TaskNotFound
from app.logger_setup import get_logger
from app.services.task import TaskService
from app.schemas.task import TaskSchema, TaskCreateSchema, TaskUpdateSchema

logger = get_logger(__name__)
router = APIRouter()


def handle_task_not_found(name: str, exception: TaskNotFound) -> None:
    """
    Handle task not found exception.
    """
    logger.warning(f"Task not found: {exception}")
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task with name '{name}' not found.",
    ) from exception


@router.get("/", response_model=list[TaskSchema])
async def get_all_tasks(
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskSchema]:
    """
    Retrieve all tasks.
    """
    tasks = await task_service.get_all_tasks()
    return tasks


@router.get("/{name}", response_model=TaskSchema)
async def get_task_by_name(  # type: ignore
    name: str,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskSchema:
    """
    Retrieve a task by its name.
    """
    try:
        return await task_service.get_task_by_name(name)
    except TaskNotFound as e:
        handle_task_not_found(name, e)


@router.post("/", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskSchema:
    """
    Create a new task.
    """
    created_task = await task_service.create_task(task_data)
    return created_task


@router.put("/{name}", response_model=TaskSchema)
async def update_task(  # type: ignore
    name: str,
    update_data: TaskUpdateSchema,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> TaskSchema:
    """
    Update a task by its name.
    """
    try:
        updated_task = await task_service.update_task(name, update_data)
        return updated_task
    except TaskNotFound as e:
        handle_task_not_found(name, e)


@router.delete("/{name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    name: str,
    task_service: Annotated[TaskService, Depends(get_task_service)],
) -> None:
    """
    Delete a task by its name.
    """
    try:
        await task_service.delete_task(name)
    except TaskNotFound as e:
        handle_task_not_found(name, e)
