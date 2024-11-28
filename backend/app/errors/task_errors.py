from typing import Any

from app.errors.base import (
    RepositoryError,
    NotFoundError,
    InvalidDataError,
    DatabaseConnectionError,
)


class TaskRepositoryError(RepositoryError):
    """
    Exception raised when a task repository operation fails.
    """

    pass


class TaskNotFound(NotFoundError):
    """
    Exception raised when a task is not found.
    """

    def __init__(self, entity: str, query: dict[str, Any]) -> None:
        super().__init__(entity, query)


class TaskDatabaseConnectionError(DatabaseConnectionError):
    """
    Exception raised when a database connection fails.
    """

    def __init__(self, message: str = "Failed to connect to the database.") -> None:
        super().__init__(message)


class InvalidTaskDataError(InvalidDataError):
    """
    Exception raised when invalid task data is provided.
    """

    def __init__(self, message: str = "Invalid task data.") -> None:
        super().__init__(message)
