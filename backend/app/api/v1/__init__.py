from fastapi import APIRouter

from .endpoints.task import router as task_router
from .endpoints.general import router as general_router

router = APIRouter()

router.include_router(router=general_router, prefix="", tags=["General"])
router.include_router(router=task_router, prefix="/tasks", tags=["Tasks"])
