from sqlalchemy.orm import Session

from app.modules.role.models import Role
from app.modules.tenant.models import Tenant, TenantUser
from app.modules.user.models import User


class TenantRepository:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # Tenant
    # -------------------------

    def get_tenant_by_slug(self, slug: str):
        return (
            self.db.query(Tenant)
            .filter(Tenant.slug == slug)
            .first()
        )

    def create_tenant(self, tenant: Tenant):
        self.db.add(tenant)
        self.db.flush()
        return tenant

    # -------------------------
    # User
    # -------------------------

    def get_user_by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def create_user(self, user: User):
        self.db.add(user)
        self.db.flush()
        return user

    # -------------------------
    # Role
    # -------------------------

    def get_role_by_name(self, role_name: str):
        return (
            self.db.query(Role)
            .filter(Role.name == role_name)
            .first()
        )

    # -------------------------
    # Tenant User
    # -------------------------

    def create_tenant_user(
        self,
        tenant_id: int,
        user_id: int,
        role_id: int,
    ):
        tenant_user = TenantUser(
            tenant_id=tenant_id,
            user_id=user_id,
            role_id=role_id,
        )

        self.db.add(tenant_user)
        self.db.flush()

        return tenant_user

    # -------------------------
    # Transaction
    # -------------------------

    def commit(self):
        self.db.commit()

    def rollback(self):
        self.db.rollback()

    def get_tenant_by_id(
    self,
    tenant_id: int,
    ) -> Tenant | None:
     return (
        self.db.query(Tenant)
        .filter(Tenant.id == tenant_id)
        .first()
    )    