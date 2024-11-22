from typing import Any
from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection


class AsyncMongoDBClient:
    """
    Asynchronous MongoDB client and database access.
    """

    def __init__(
        self,
        uri: str = "mongodb://localhost:27017/",
        database_name: str = "task_database",
    ):
        self._client: AsyncMongoClient[Any] = AsyncMongoClient(uri)
        self.database_name = database_name
        self._connected = False

    async def connect(self) -> None:
        """Explicitly connects to the MongoDB server."""
        if not self._connected:
            await self._client.aconnect()
            self._connected = True

    async def get_collection(
        self, collection_name: str
    ) -> AsyncCollection[dict[str, Any]]:
        """
        Returns a collection from the database.
        """
        if not self._connected:
            raise RuntimeError(
                "MongoDB client is not connected. Call `connect()` first."
            )

        database = self._client[self.database_name]
        return database[collection_name]

    async def close(self) -> None:
        """Closes the MongoDB client."""
        await self._client.close()
        self._connected = False
