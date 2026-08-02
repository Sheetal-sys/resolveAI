from fastapi import HTTPException, status

from app.modules.auth.schemas import CurrentUserResponse
from app.modules.tenant_settings.repositories import TenantSettingsRepository
from app.modules.tenant_settings.schemas import (
    TenantSettingsResponse,
    UpdateTenantSettingsRequest,
)


class UpdateTenantSettingsService:
    def __init__(
        self,
        repository: TenantSettingsRepository,
    ):
        self.repository = repository

    def update_settings(
        self,
        request: UpdateTenantSettingsRequest,
        current_user: CurrentUserResponse,
    ) -> TenantSettingsResponse:
        tenant_settings = self.repository.get_by_tenant_id(
            tenant_id=current_user.tenant_id,
        )

        if tenant_settings is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant settings not found",
            )

        update_data = request.model_dump(
            exclude_unset=True,
        )

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No settings were provided for update",
            )

        for field, value in update_data.items():
            if field in {"website", "logo_url"} and value is not None:
                value = str(value)

            if field == "currency" and value is not None:
                value = value.upper().strip()

            if field in {"timezone", "language"} and value is not None:
                value = value.strip()

            if field == "support_phone" and value is not None:
                value = value.strip()

            setattr(
                tenant_settings,
                field,
                value,
            )

        if (
            tenant_settings.business_start_time
            >= tenant_settings.business_end_time
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    "business_start_time must be earlier "
                    "than business_end_time"
                ),
            )

        try:
            tenant_settings = self.repository.update(
                tenant_settings
            )

            self.repository.commit()
            self.repository.refresh(tenant_settings)

            return TenantSettingsResponse(
                tenant_id=tenant_settings.tenant_id,
                company_name=current_user.tenant_name,
                website=tenant_settings.website,
                support_email=tenant_settings.support_email,
                support_phone=tenant_settings.support_phone,
                timezone=tenant_settings.timezone,
                language=tenant_settings.language,
                currency=tenant_settings.currency,
                business_start_time=tenant_settings.business_start_time,
                business_end_time=tenant_settings.business_end_time,
                logo_url=tenant_settings.logo_url,
                ai_confidence_threshold=(
                    tenant_settings.ai_confidence_threshold
                ),
                auto_reply=tenant_settings.auto_reply,
                auto_escalation=tenant_settings.auto_escalation,
            )

        except HTTPException:
            self.repository.rollback()
            raise

        except Exception as exc:
            self.repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Tenant settings update failed: {str(exc)}",
            ) from exc