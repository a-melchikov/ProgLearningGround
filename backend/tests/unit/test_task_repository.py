import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from pymongo import errors
from pymongo.asynchronous.collection import AsyncCollection

from app.db.database import AsyncMongoDBClient
from app.errors.task_errors import TaskNotFound, DatabaseConnectionError
from app.repositories.task import TaskRepository


@pytest.fixture
def mock_db_client():
    with patch("app.db.database.AsyncMongoClient") as mock_client:
        client = AsyncMongoDBClient()
        client._connected = True
        client._client = mock_client
        mock_collection = AsyncMock(spec=AsyncCollection)
        client.get_collection = AsyncMock(return_value=mock_collection)
        yield client


@pytest.fixture
def task_repository(mock_db_client):
    return TaskRepository(mock_db_client)


@pytest.mark.asyncio
async def test_get_task_success(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_collection.find_one.return_value = {
        "name": "test_task",
        "description": "Test description",
    }

    result = await task_repository.find_one({"name": "test_task"})

    assert result == {"name": "test_task", "description": "Test description"}
    mock_collection.find_one.assert_called_once_with({"name": "test_task"})


@pytest.mark.asyncio
async def test_get_task_not_found(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_collection.find_one.return_value = None

    with pytest.raises(TaskNotFound):
        await task_repository.find_one({"name": "non_existent_task"})


@pytest.mark.asyncio
async def test_get_task_database_error(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_collection.find_one.side_effect = errors.PyMongoError("Database error")

    with pytest.raises(DatabaseConnectionError):
        await task_repository.find_one({"name": "test_task"})


@pytest.mark.asyncio
async def test_get_tasks_success(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_cursor = AsyncMock()
    mock_cursor.to_list.return_value = [{"name": "task1"}, {"name": "task2"}]
    mock_collection.find.return_value = mock_cursor

    result = await task_repository.find_all()

    assert result == [{"name": "task1"}, {"name": "task2"}]
    mock_collection.find.assert_called_once_with({}, {})


@pytest.mark.asyncio
async def test_get_only_task_names_success(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_cursor = AsyncMock()
    mock_cursor.to_list.return_value = [
        {"name": "task1"},
        {"name": "task2"},
        {"name": "task3"},
    ]
    mock_collection.find.return_value = mock_cursor

    expected_result = [
        {"name": "task1"},
        {"name": "task2"},
        {"name": "task3"},
    ]
    projection = {"name": True, "description": False}

    result = await task_repository.find_all(projection=projection)
    assert result == expected_result
    mock_collection.find.assert_called_once_with({}, projection)


@pytest.mark.asyncio
async def test_create_task_success(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_collection.insert_one.return_value = MagicMock(inserted_id="new_id")

    task_data = {"name": "new_task", "description": "New task description"}
    result = await task_repository.add_one(task_data)

    assert result == {
        "name": "new_task",
        "description": "New task description",
        "_id": "new_id",
    }
    mock_collection.insert_one.assert_called_once_with(task_data)


@pytest.mark.asyncio
async def test_update_task_success(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_collection.update_one.return_value = MagicMock(matched_count=1)
    mock_collection.find_one.return_value = {
        "name": "updated_task",
        "description": "Updated description",
    }

    update_data = {"description": "Updated description"}
    result = await task_repository.update_one({"name": "existing_task"}, update_data)

    assert result == {"name": "updated_task", "description": "Updated description"}
    mock_collection.update_one.assert_called_once_with(
        {"name": "existing_task"}, {"$set": update_data}
    )


@pytest.mark.asyncio
async def test_update_task_not_found(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_collection.update_one.return_value = MagicMock(matched_count=0)

    with pytest.raises(TaskNotFound):
        await task_repository.update_one(
            {"name": "non_existent_task"}, {"description": "Updated description"}
        )


@pytest.mark.asyncio
async def test_delete_task_success(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_collection.delete_one.return_value = MagicMock(deleted_count=1)

    await task_repository.delete_one({"name": "existing_task"})

    mock_collection.delete_one.assert_called_once_with({"name": "existing_task"})


@pytest.mark.asyncio
async def test_delete_task_not_found(task_repository):
    mock_collection = await task_repository.db_client.get_collection("tasks")
    mock_collection.delete_one.return_value = MagicMock(deleted_count=0)

    with pytest.raises(TaskNotFound):
        await task_repository.delete_one({"name": "non_existent_task"})
