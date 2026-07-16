from fastapi import HTTPException, status

from app.core.security import hash_password
from app.modules.tenant.models import Tenant
from app.modules.tenant.repository import TenantRepository
from app.modules.tenant.schemas import (
    TenantRegisterRequest,
    TenantRegisterResponse,
)
from app.modules.tenant_settings.repositories import TenantSettingsRepository
from app.modules.tenant_settings.services import (
    CreateDefaultTenantSettingsService,
)
from app.modules.user.models import User
from app.shared.base.enums import RoleName


class TenantService:
    def __init__(self, repository: TenantRepository):
        self.repository = repository

    def register_tenant(
        self,
        request: TenantRegisterRequest,
    ) -> TenantRegisterResponse:
        existing_tenant = self.repository.get_tenant_by_slug(
            request.company_slug
        )

        if existing_tenant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Company slug already exists",
            )

        existing_user = self.repository.get_user_by_email(
            request.admin_email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Admin email already exists",
            )

        tenant_admin_role = self.repository.get_role_by_name(
            RoleName.TENANT_ADMIN.value
        )

        if not tenant_admin_role:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    "TENANT_ADMIN role not found. "
                    "Please seed roles first."
                ),
            )

        try:
            tenant = Tenant(
                name=request.company_name.strip(),
                slug=request.company_slug.lower().strip(),
            )

            tenant = self.repository.create_tenant(tenant)

            admin_user = User(
                first_name=request.admin_first_name.strip(),
                last_name=(
                    request.admin_last_name.strip()
                    if request.admin_last_name
                    else None
                ),
                email=request.admin_email.lower().strip(),
                password_hash=hash_password(
                    request.admin_password
                ),
                is_active=True,
            )

            admin_user = self.repository.create_user(admin_user)

            self.repository.create_tenant_user(
                tenant_id=tenant.id,
                user_id=admin_user.id,
                role_id=tenant_admin_role.id,
            )

            tenant_settings_repository = TenantSettingsRepository(
                self.repository.db
            )

            tenant_settings_service = (
                CreateDefaultTenantSettingsService(
                    tenant_settings_repository
                )
            )

            tenant_settings_service.create_for_tenant(
                tenant_id=tenant.id,
                commit=False,
            )

            self.repository.commit()

            return TenantRegisterResponse(
                tenant_id=tenant.id,
                company_name=tenant.name,
                company_slug=tenant.slug,
                admin_email=admin_user.email,
                message="Tenant registered successfully",
            )

        except HTTPException:
            self.repository.rollback()
            raise

        except Exception as exc:
            self.repository.rollback()

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Tenant registration failed: {str(exc)}",
            ) from exc