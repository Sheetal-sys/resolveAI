from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.tenant.models import Tenant
from app.modules.tenant.repository import TenantRepository
from app.modules.tenant_settings.repositories import TenantSettingsRepository
from app.modules.tenant_settings.schemas import TenantSettingsResponse


class GetTenantSettingsService:
    def __init__(
        self,
        settings_repository: TenantSettingsRepository,
        tenant_repository: TenantRepository,
    ):
        self.settings_repository = settings_repository
        self.tenant_repository = tenant_repository

    def get_settings(
        self,
        current_user: CurrentUserResponse,
    ) -> TenantSettingsResponse:
        tenant_settings = self.settings_repository.get_by_tenant_id(
            tenant_id=current_user.tenant_id,
        )

        if tenant_settings is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant settings not found",
            )

        tenant: Tenant | None = self.tenant_repository.get_tenant_by_id(
            tenant_id=current_user.tenant_id,
        )

        if tenant is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found",
            )

        return TenantSettingsResponse(
            tenant_id=tenant_settings.tenant_id,
            company_name=tenant.name,
            website=tenant_settings.website,
            support_email=tenant_settings.support_email,
            support_phone=tenant_settings.support_phone,
            timezone=tenant_settings.timezone,
            language=tenant_settings.language,
            currency=tenant_settings.currency,
            business_start_time=tenant_settings.business_start_time,
            business_end_time=tenant_settings.business_end_time,
            logo_url=tenant_settings.logo_url,
            ai_confidence_threshold=tenant_settings.ai_confidence_threshold,
            auto_reply=tenant_settings.auto_reply,
            auto_escalation=tenant_settings.auto_escalation,
        )