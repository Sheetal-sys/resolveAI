from fastapi import APIRouter

from app.modules.user.api.create_user import router as create_user_router
from app.modules.user.api.list_users import router as list_users_router
from app.modules.user.api.get_user import router as get_user_router
from app.modules.user.api.update_user import router as update_user_router
from app.modules.user.api.change_role import router as change_role_router
from app.modules.user.api.change_status import router as change_status_router
from app.modules.user.api.reset_password import router as reset_password_router
from app.modules.user.api.remove_user import router as remove_user_router

router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],
)

router.include_router(create_user_router)
router.include_router(list_users_router)
router.include_router(get_user_router)
router.include_router(update_user_router)
router.include_router(change_role_router)
router.include_router(change_status_router)
router.include_router(reset_password_router)
router.include_router(remove_user_router)

__all__ = ["router"]