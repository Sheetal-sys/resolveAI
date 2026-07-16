from sqlalchemy.orm import Session

from app.modules.tenant_settings.models import TenantSettings


class TenantSettingsRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_tenant_id(
        self,
        tenant_id: int,
    ) -> TenantSettings | None:
        return (
            self.db.query(TenantSettings)
            .filter(TenantSettings.tenant_id == tenant_id)
            .first()
        )

    def create_default_settings(
        self,
        tenant_id: int,
    ) -> TenantSettings:
        tenant_settings = TenantSettings(
            tenant_id=tenant_id,
        )

        self.db.add(tenant_settings)
        self.db.flush()

        return tenant_settings

    def update(
        self,
        tenant_settings: TenantSettings,
    ) -> TenantSettings:
        self.db.add(tenant_settings)
        self.db.flush()

        return tenant_settings

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()

    def refresh(
        self,
        tenant_settings: TenantSettings,
    ) -> None:
        self.db.refresh(tenant_settings)