import platform

from datetime import datetime
from fastapi import APIRouter, HTTPException

from app.db.database import AsyncMongoDBClient
from app.core.logger_setup import get_logger

logger = get_logger(__name__)

router = APIRouter()

START_TIME = datetime.utcnow()

mongo_client = AsyncMongoDBClient()


@router.get(
    "/",
    response_model=dict[str, str],
)
async def root() -> dict[str, str]:
    """
    Root endpoint providing general application information.

    Returns:
        dict[str, str]: A dictionary with application details.
    """
    return {
        "app_name": "Task API",
        "version": "1.0.0",
        "start_time": START_TIME.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "current_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "server": platform.node(),
        "os": platform.system(),
        "python_version": platform.python_version(),
        "description": "API for task management.",
    }


@router.get(
    "/healthcheck",
    response_model=dict[str, str],
)
async def healthcheck() -> dict[str, str]:
    """
    Healthcheck endpoint to verify the status of MongoDB connection.

    Returns:
        dict[str, str]: Status of the MongoDB connection.
    """
    try:
        await mongo_client.connect()
        test_collection = await mongo_client.get_collection("test")
        await test_collection.count_documents({})
        return {"status": "Healthy", "database": "Connected"}
    except Exception as e:
        logger.error(f"Healthcheck failed: {e}")
        raise HTTPException(
            status_code=503, detail="Database connection failed."
        ) from e
