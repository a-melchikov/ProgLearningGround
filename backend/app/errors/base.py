from typing import Any


class BaseError(Exception):
    """
    Base class for all custom exceptions.
    """

    def __init__(self, message: str, *args: Any) -> None:
        super().__init__(message, *args)


class RepositoryError(BaseError):
    """
    Base class for all repository-related exceptions.
    """

    pass


class NotFoundError(RepositoryError):
    """
    Base class for all "not found" exceptions.
    """

    def __init__(self, entity: str, query: dict[str, Any]) -> None:
        message = f"{entity} with query '{query}' not found."
        super().__init__(message)


class DatabaseConnectionError(RepositoryError):
    """
    Base class for all connection-related exceptions.
    """

    def __init__(self, message: str = "Failed to establish a connection.") -> None:
        super().__init__(message)


class InvalidDataError(BaseError):
    """
    Base class for all invalid data exceptions.
    """

    def __init__(self, message: str = "Invalid data provided.") -> None:
        super().__init__(message)
