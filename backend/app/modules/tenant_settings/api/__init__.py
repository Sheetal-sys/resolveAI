from fastapi import APIRouter

from app.modules.tenant_settings.api.get_settings import (
    router as get_settings_router,
)
from app.modules.tenant_settings.api.update_settings import (
    router as update_settings_router,
)

router = APIRouter(
    prefix="/settings",
    tags=["Tenant Settings"],
)

router.include_router(get_settings_router)
router.include_router(update_settings_router)

__all__ = ["router"]