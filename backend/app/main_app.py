import json

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ValidationError
from typing import Any

from starlette.middleware.cors import CORSMiddleware

from app.middlewares.exception_middleware import ExceptionMiddleware
from app.middlewares.logging_middleware import LoggingMiddleware
from logger_setup import get_logger
from task_runner import run_code_in_docker
from task_data_loader import get_all_tasks_name, open_tasks_json
from api.v1 import router as router_v1

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


class Code(BaseModel):
    code: str = Field(
        ...,
        title="User Code",
        description="The code to be executed.",
        examples=[
            'number = int(input())\nreversed_number = int(str(number)[::-1])\nprint(f"{number} + {reversed_number} = {number + reversed_number}")',
        ],
    )


@app.get(
    "/",
    tags=["General"],
    response_model=dict[str, str],
)
async def root() -> dict[str, str]:
    """
    Root endpoint to check the status of the API.

    Returns:
        A greeting message.
    """
    logger.info("Root endpoint accessed.")
    return {"Hello": "World"}


@app.post(
    "/send_task/{task_name}/",
    tags=["Tasks"],
    response_model=dict[str, Any],
)
async def send_task(task_name: str, code: Code) -> dict[str, Any]:
    """
    Endpoint to execute user code against a specific task.

    Args:
        task_name (str): The name of the task.
        code (Code): User-submitted code.

    Returns:
        dict[str, Any]: The result of the execution or an error message.

    Raises:
        HTTPException: If execution fails or the task does not exist.
    """
    logger.info(f"Received task '{task_name}' with user code.")
    try:
        result = run_code_in_docker(task_name, code.code)
        logger.info(f"Execution completed for task '{task_name}'. Result: {result}")
        return {"result": result}
    except ValidationError as ve:
        logger.error(f"Validation error for task '{task_name}': {ve}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Validation Error: {ve.errors()}",
        ) from ve
    except FileNotFoundError as fe:
        logger.error(f"Task file not found for '{task_name}': {fe}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_name}' not found.",
        ) from fe
    except Exception as e:
        logger.exception(f"Error while executing task '{task_name}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        ) from e


@app.get(
    "/tasks/",
    tags=["Tasks"],
    response_model=list[str],
)
async def get_tasks() -> list[str]:
    """
    Endpoint to retrieve the list of available tasks.

    Returns:
        list[str]: A list of available tasks.
    """
    logger.info("Fetching list of tasks.")
    try:
        task_names: list[str] = get_all_tasks_name()
        return task_names
    except FileNotFoundError as e:
        logger.error(f"Tasks file not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tasks file not found.",
        ) from e
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding tasks JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error decoding tasks JSON.",
        ) from e


@app.get(
    "/task_details/{task_name}/",
    tags=["Tasks"],
    response_model=dict[str, Any],
)
async def get_task_details(task_name: str) -> dict[str, Any]:
    """
    Endpoint to retrieve task details.

    Args:
        task_name (str): The name of the task.

    Returns:
        dict[str, Any]: A task details.
    """
    logger.info(f"Fetching details for task: {task_name}")
    try:
        task_details: dict[str, Any] = open_tasks_json(task_name=task_name)
        return task_details
    except FileNotFoundError as e:
        logger.error(f"Task not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_name}' not found.",
        ) from e
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding task JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error decoding task JSON.",
        ) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
