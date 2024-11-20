__all__ = [
    "open_tasks_json",
    "DESCRIPTION",
    "INPUT",
    "OUTPUT",
    "EXAMPLES",
    "TEST_CASES",
]

import json
from typing import Any
from pathlib import Path
from logger_setup import get_logger

logger = get_logger(__name__)

DESCRIPTION = "description"
INPUT = "input"
OUTPUT = "expected_output"
EXAMPLES = "examples"
TEST_CASES = "test_cases"


def open_tasks_json(task_name: str, json_name: str = "tasks.json") -> dict[str, Any]:
    """
    Opens a JSON file with tasks and returns data for the specified task.

    Args:
        task_name (str): The name of the task.
        json_name (str): The name of the JSON file.

    Raises:
        FileNotFoundError: If the file is not found.
        ValueError: If the file contains invalid JSON.
        KeyError: If the task is not found in the JSON.
    """
    task_path = Path.cwd() / json_name
    logger.info(f"Opening JSON file at path {task_path}")
    if not task_path.is_file():
        logger.error(f"File {json_name} not found at path {task_path}")
        raise FileNotFoundError(f"Task file {json_name} not found at {task_path}")

    try:
        with open(task_path, "r", encoding="utf-8") as f:
            data: dict[str, Any] = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error in file {json_name}: {e}")
        raise ValueError(f"Invalid JSON format in file {json_name}") from e

    if task_name not in data:
        logger.error(f"Task '{task_name}' not found in JSON file {json_name}")
        raise KeyError(f"Task '{task_name}' not found in {json_name}")

    task_data: dict[str, Any] = data[task_name]
    description = task_data.get(DESCRIPTION, "No description provided")
    examples = task_data.get(EXAMPLES, "No examples provided")

    logger.info(f"Task description: {description}")
    logger.info(f"Task examples: {examples}")

    return task_data
