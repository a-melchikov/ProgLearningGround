from abc import ABC, abstractmethod
from typing import Any

from pymongo import errors
from pymongo.asynchronous.collection import AsyncCollection

from app.db.database import AsyncMongoDBClient
from app.errors.base import NotFoundError, DatabaseConnectionError
from app.core.logger_setup import get_logger

logger = get_logger(__name__)


class AbstractRepository(ABC):
    """
    Interface for all repositories
    """

    @abstractmethod
    async def add_one(self, data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, filter_query: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def find_all(
        self, filter_query: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def update_one(
        self, filter_query: dict[str, Any], update_data: dict[str, Any]
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, filter_query: dict[str, Any]) -> None:
        raise NotImplementedError


class MongoDBRepository(AbstractRepository):
    """
    Base repository for MongoDB
    """

    def __init__(
        self,
        db_client: AsyncMongoDBClient,
        collection_name: str,
        log_name: str,
        not_found_error: type[NotFoundError],
        database_connection_error: type[DatabaseConnectionError],
    ) -> None:
        self.db_client = db_client
        self.collection_name = collection_name
        self.log_name = log_name.lower()
        self.not_found_error = not_found_error
        self.database_connection_error = database_connection_error

    async def _get_collection(self) -> AsyncCollection[dict[str, Any]]:
        """
        Internal method to get the collection instance.
        """
        try:
            return await self.db_client.get_collection(self.collection_name)
        except errors.PyMongoError as e:
            logger.error(
                f"Error while accessing collection '{self.collection_name}': {str(e)}"
            )
            raise self.database_connection_error(
                f"Error while accessing collection '{self.collection_name}': {str(e)}"
            ) from e

    async def add_one(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Adds a single document to the collection.
        """
        try:
            collection = await self._get_collection()
            result = await collection.insert_one(data)
            data["_id"] = str(result.inserted_id)
            logger.info(f"Created {self.log_name} with data: {data}")
            return data
        except errors.PyMongoError as e:
            logger.error(f"Database error while creating {self.log_name}: {str(e)}")
            raise self.database_connection_error(
                f"Error while inserting {self.log_name} data: {str(e)}"
            ) from e

    async def find_one(self, filter_query: dict[str, Any]) -> dict[str, Any]:
        """
        Finds a single document in the collection based on a filter query.
        """
        try:
            collection = await self._get_collection()
            document = await collection.find_one(filter_query)
            if not document:
                logger.info(
                    f"{self.log_name.capitalize()} not found for query: {filter_query}"
                )
                raise self.not_found_error(
                    entity=self.log_name.capitalize(),
                    query=filter_query,
                )
            logger.info(f"Found {self.log_name}: {document}")
            return document
        except self.not_found_error as e:
            raise e
        except errors.PyMongoError as e:
            logger.error(f"Database error while fetching {self.log_name}: {str(e)}")
            raise self.database_connection_error(
                f"Error while accessing database for {self.log_name}: {str(e)}"
            ) from e

    async def find_all(
        self, filter_query: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """
        Finds all documents in the collection that match the filter query.
        """
        try:
            collection = await self._get_collection()
            cursor = collection.find(filter_query or {})
            documents = await cursor.to_list(length=None)
            logger.info(
                f"Found {len(documents)} {self.log_name}(s) for query: {filter_query}"
            )
            return documents
        except errors.PyMongoError as e:
            logger.error(
                f"Database error while fetching all {self.log_name}s: {str(e)}"
            )
            raise self.database_connection_error(
                f"Error while accessing database for all {self.log_name}s: {str(e)}"
            ) from e

    async def update_one(
        self, filter_query: dict[str, Any], update_data: dict[str, Any]
    ) -> Any:
        """
        Updates a single document in the collection based on a filter query.
        """
        try:
            collection = await self._get_collection()
            result = await collection.update_one(filter_query, {"$set": update_data})
            if result.matched_count == 0:
                logger.info(
                    f"{self.log_name.capitalize()} not found for update: {filter_query}"
                )
                raise self.not_found_error(
                    entity=self.log_name.capitalize(),
                    query=filter_query,
                )
            updated_document = await collection.find_one(filter_query)
            logger.info(f"Updated {self.log_name}: {updated_document}")
            return updated_document
        except self.not_found_error as e:
            raise e
        except errors.PyMongoError as e:
            logger.error(f"Database error while updating {self.log_name}: {str(e)}")
            raise self.database_connection_error(
                f"Error while updating {self.log_name}: {str(e)}"
            ) from e

    async def delete_one(self, filter_query: dict[str, Any]) -> None:
        """
        Deletes a single document in the collection based on a filter query.
        """
        try:
            collection = await self._get_collection()
            result = await collection.delete_one(filter_query)
            if result.deleted_count == 0:
                logger.info(
                    f"{self.log_name.capitalize()} not found for deletion: {filter_query}"
                )
                raise self.not_found_error(
                    entity=self.log_name.capitalize(),
                    query=filter_query,
                )
            logger.info(f"Deleted {self.log_name} with query: {filter_query}")
        except self.not_found_error as e:
            raise e
        except errors.PyMongoError as e:
            logger.error(f"Database error while deleting {self.log_name}: {str(e)}")
            raise self.database_connection_error(
                f"Error while deleting {self.log_name}: {str(e)}"
            ) from e
