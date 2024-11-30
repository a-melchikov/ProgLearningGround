from typing import Any
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection

from app.core.logger_setup import get_logger
from app.core.config import settings

logger = get_logger(__name__)


class AsyncMongoDBClient:
    """
    Asynchronous MongoDB client and database access.
    """

    def __init__(
        self,
        database_name: str = settings.MONG0_DB_NAME,
    ):
        self.uri = settings.get_mongo_db_url()
        self._client: AsyncMongoClient[Any] = AsyncMongoClient(self.uri)
        self.database_name = database_name
        self._connected = False
        logger.info(
            f"Initialized AsyncMongoDBClient with URI: {self.uri} and database: {database_name}"
        )

    async def connect(self) -> None:
        """Explicitly connects to the MongoDB server."""
        if not self._connected:
            address = await self._client.address
            logger.info(f"Connecting to MongoDB server at {address}...")
            await self._client.aconnect()
            self._connected = True
            logger.info(f"Successfully connected to MongoDB server at {address}")

    async def get_collection(
        self, collection_name: str
    ) -> AsyncCollection[dict[str, Any]]:
        """
        Returns a collection from the database.
        """
        if not self._connected:
            logger.warning("MongoDB client is not connected")
            raise RuntimeError(
                "MongoDB client is not connected. Call `connect()` first."
            )
        logger.info(
            f"Getting collection '{collection_name}' from database: '{self.database_name}'"
        )
        database = self._client[self.database_name]
        collection = database[collection_name]
        logger.info(f"Successfully retrieved collection '{collection_name}'")
        return collection

    async def close(self) -> None:
        """Closes the MongoDB client."""
        if self._connected:
            address = await self._client.address
            logger.info(f"Closing MongoDB client at {address}")
            await self._client.close()
            self._connected = False
            logger.info("Successfully closed MongoDB client")
        else:
            logger.warning(
                "Attempted to close MongoDB connection, but client is not connected."
            )


db_client = AsyncMongoDBClient()
