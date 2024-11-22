import pytest
from unittest.mock import AsyncMock, patch
from pymongo.errors import ConnectionFailure
import re

from app.database import AsyncMongoDBClient


@pytest.mark.asyncio
async def test_connect_success():
    """Check database connection success"""
    with patch(
        "app.database.AsyncMongoClient.aconnect", new_callable=AsyncMock
    ) as mock_connect:
        client = AsyncMongoDBClient()
        await client.connect()
        mock_connect.assert_called_once()
        assert client._connected is True


@pytest.mark.asyncio
async def test_connect_already_connected():
    """Check database connection when already connected"""
    with patch(
        "app.database.AsyncMongoClient.aconnect", new_callable=AsyncMock
    ) as mock_connect:
        client = AsyncMongoDBClient()
        client._connected = True
        await client.connect()
        mock_connect.assert_not_called()


@pytest.mark.asyncio
async def test_get_collection_success():
    """Check database collection retrieval success"""
    mock_db = AsyncMock()
    mock_collection = AsyncMock()
    with patch("app.database.AsyncMongoClient.__getitem__", return_value=mock_db):
        mock_db.__getitem__.return_value = mock_collection

        client = AsyncMongoDBClient()
        client._connected = True

        collection = await client.get_collection("test_collection")

        mock_db.__getitem__.assert_called_once_with("test_collection")
        assert collection == mock_collection


@pytest.mark.asyncio
async def test_get_collection_without_connection():
    """Check database collection retrieval without successful connection"""
    client = AsyncMongoDBClient()

    with pytest.raises(
        RuntimeError,
        match=re.escape("MongoDB client is not connected. Call `connect()` first."),
    ):
        await client.get_collection("test_collection")


@pytest.mark.asyncio
async def test_close():
    """Check database connection closing success"""
    with patch(
        "app.database.AsyncMongoClient.close", new_callable=AsyncMock
    ) as mock_close:
        client = AsyncMongoDBClient()
        client._connected = True

        await client.close()
        mock_close.assert_called_once()
        assert client._connected is False


@pytest.mark.asyncio
async def test_connect_failure():
    """Check database connection failure"""
    with patch(
        "app.database.AsyncMongoClient.aconnect",
        new_callable=AsyncMock,
        side_effect=ConnectionFailure,
    ):
        client = AsyncMongoDBClient()

        with pytest.raises(ConnectionFailure):
            await client.connect()
        assert client._connected is False
