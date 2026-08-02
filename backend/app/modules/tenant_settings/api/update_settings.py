from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.auth.schemas import CurrentUserResponse
from app.modules.tenant_settings.repositories import (
    TenantSettingsRepository,
)
from app.modules.tenant_settings.schemas import (
    TenantSettingsResponse,
    UpdateTenantSettingsRequest,
)
from app.modules.tenant_settings.services import (
    UpdateTenantSettingsService,
)
from app.shared.base.enums import RoleName

router = APIRouter()


@router.patch(
    "/",
    response_model=TenantSettingsResponse,
)
def update_settings(
    request: UpdateTenantSettingsRequest,
    db: Session = Depends(get_db),
    current_user: CurrentUserResponse = Depends(
        require_roles([RoleName.TENANT_ADMIN.value])
    ),
):
    repository = TenantSettingsRepository(db)
    service = UpdateTenantSettingsService(repository)

    return service.update_settings(
        request=request,
        current_user=current_user,
    )