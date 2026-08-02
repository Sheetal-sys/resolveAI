from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.tenant.repository import TenantRepository
from app.modules.tenant_settings.repositories import (
    TenantSettingsRepository,
)
from app.modules.tenant_settings.schemas import (
    TenantSettingsResponse,
)
from app.modules.tenant_settings.services import (
    GetTenantSettingsService,
)

router = APIRouter()


@router.get(
    "/",
    response_model=TenantSettingsResponse,
)
def get_settings(
    current_user: CurrentUserResponse = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    settings_repository = TenantSettingsRepository(db)
    tenant_repository = TenantRepository(db)

    service = GetTenantSettingsService(
        settings_repository=settings_repository,
        tenant_repository=tenant_repository,
    )

    return service.get_settings(current_user)