from fastapi import APIRouter

from .endpoints.task import router as task_router

router = APIRouter()

router.include_router(router=task_router, prefix="/tasks", tags=["Tasks"])
