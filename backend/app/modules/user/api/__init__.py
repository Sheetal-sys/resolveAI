from fastapi import APIRouter

from app.modules.user.api.create_user import router as create_user_router
from app.modules.user.api.list_users import router as list_users_router

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)

router.include_router(create_user_router)
router.include_router(list_users_router)

__all__ = ["router"]