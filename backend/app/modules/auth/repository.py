from sqlalchemy.orm import Session

from app.modules.role.models import Role
from app.modules.tenant.models import Tenant, TenantUser
from app.modules.user.models import User


class AuthRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_user_by_id(self, user_id: int):
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_user_tenant_role(self, user_id: int):
        return (
            self.db.query(TenantUser, Tenant, Role)
            .join(Tenant, TenantUser.tenant_id == Tenant.id)
            .join(Role, TenantUser.role_id == Role.id)
            .filter(TenantUser.user_id == user_id)
            .first()
        )