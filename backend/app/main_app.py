from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ValidationError
from typing import Any

from logger_setup import get_logger
from task_runner import run_code_in_docker

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
    tags=["Task Execution"],
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main_app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
