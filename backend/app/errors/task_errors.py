from typing import Any


class TaskRepositoryError(Exception):
    """
    Exception raised when a task repository operation fails.
    """

    def __init__(self, message: str, *args: Any) -> None:
        super().__init__(message, *args)


class TaskNotFound(TaskRepositoryError):
    """
    Exception raised when a task is not found.
    """

    def __init__(self, task_name: str) -> None:
        message = f"Task '{task_name}' not found."
        super().__init__(message)


class DatabaseConnectionError(TaskRepositoryError):
    """
    Exception raised when a database connection fails.
    """

    def __init__(self, message: str = "Failed to connect to the database.") -> None:
        super().__init__(message)


class InvalidTaskDataError(TaskRepositoryError):
    """
    Exception raised when invalid task data is provided.
    """

    def __init__(self, message: str = "Invalid task data.") -> None:
        super().__init__(message)
