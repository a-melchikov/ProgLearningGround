import asyncio
from typing import Any

import httpx
import docker

from fastapi import HTTPException, status

from app.utils.code_tester import get_testing_code
from app.core.logger_setup import get_logger

logger = get_logger(__name__)
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"


async def fetch_task_by_name(name: str) -> dict[str, Any]:
    """
    Sends a request to fetch a task by its name.

    Args:
        name (str): Name of the task.

    Returns:
        dict: Task data if found.

    Raises:
        HTTPException: If the request fails or task not found.
    """
    async with httpx.AsyncClient() as client:
        url = f"{BASE_URL}{API_PREFIX}/tasks/{name}"
        logger.info(f"Fetching task from '{url}'.")
        response = await client.get(url)
        response.raise_for_status()
        task_data: dict[str, Any] = response.json()
        logger.info(f"Task data fetched successfully for '{name}'.")
        return task_data


async def run_code_in_docker(task_name: str, user_code: str) -> str:
    """
    Runs the user's code in a Docker container and validates it against test cases.

    Args:
        task_name (str): The name of the task to be tested.
        user_code (str): The user's Python code as a string.

    Returns:
        str: A summary string indicating the number and percentage of tests passed.
    """
    client = docker.from_env()
    passed_tests = 0

    try:
        data = await fetch_task_by_name(task_name)
        logger.info(f"Loaded task '{task_name}' successfully.")
    except httpx.HTTPStatusError as e:
        logger.error(
            f"HTTP error while fetching task '{task_name}': {e.response.status_code} - {e.response.text}"
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_name}' not found",
        ) from e
    except ValueError as e:
        logger.error(f"Failed to parse JSON for task '{task_name}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error parsing JSON",
        ) from e

    test_cases: list[dict[str, str]] = data.get("test_cases", [])
    logger.debug("Test cases: {}".format(test_cases))

    if not test_cases:
        logger.warning(f"No test cases found for task '{task_name}'.")
        return "Warning: No test cases found."

    for idx, test_case in enumerate(test_cases, start=1):
        test_input = test_case["input"]
        expected_output = test_case["expected_output"]

        test_script = get_testing_code(user_code, test_input, expected_output)

        try:
            logger.info(f"Running test case {idx} with input: {test_input}")
            container = client.containers.run(
                "python:3.12-slim",
                command=["python", "-c", test_script],
                detach=True,
                stderr=True,
                stdout=True,
                remove=True,
                mem_limit="128m",
                cpu_quota=50000,
            )
            container.wait()
            logs = container.logs().decode("utf-8").strip()

            logger.debug(f"Container logs for test case {idx}: {logs}")

            if "PASS" in logs:
                passed_tests += 1
                logger.info(f"Test case {idx} passed.")
            else:
                logger.warning(
                    f"Test case {idx} failed. Expected: {expected_output}, Got: {logs}"
                )
        except docker.errors.ContainerError as e:
            logger.error(
                f"Test case {idx} failed due to a container error: {e.stderr.decode('utf-8')}"
            )
        except docker.errors.DockerException as e:
            logger.error(f"Test case {idx} failed due to a Docker error: {str(e)}")

    total_tests = len(test_cases)
    percentage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    result_string = (
        f"{passed_tests} out of {total_tests} tests passed ({percentage:.2f}%)."
    )
    logger.info(f"Testing summary for {task_name}: {result_string}")
    client.close()
    return result_string


if __name__ == "__main__":
    task_name = "sum_with_inversion"

    user_code = """
number = int(input())
reversed_number = int(str(number)[::-1])
print(f"{number} + {reversed_number} = {number + reversed_number}")
    """

    result = asyncio.run(run_code_in_docker(task_name, user_code))
    print(result)
