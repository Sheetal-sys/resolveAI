from fastapi import HTTPException, status

from app.modules.tenant_settings.models import TenantSettings
from app.modules.tenant_settings.repositories import TenantSettingsRepository


class CreateDefaultTenantSettingsService:
    def __init__(self, repository: TenantSettingsRepository):
        self.repository = repository

    def create_for_tenant(
        self,
        tenant_id: int,
        commit: bool = True,
    ) -> TenantSettings:
        existing_settings = self.repository.get_by_tenant_id(
            tenant_id=tenant_id,
        )

        if existing_settings:
            return existing_settings

        try:
            tenant_settings = self.repository.create_default_settings(
                tenant_id=tenant_id,
            )

            if commit:
                self.repository.commit()
                self.repository.refresh(tenant_settings)

            return tenant_settings

        except Exception as exc:
            if commit:
                self.repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Default tenant settings creation failed: {str(exc)}",
            ) from exc