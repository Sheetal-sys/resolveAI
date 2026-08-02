from app.modules.role.models import Role
from app.modules.tenant.models import Tenant, TenantUser
from app.modules.tenant_settings.models import TenantSettings
from app.modules.user.models import User


def test_database_table_names() -> None:
    assert Role.__tablename__ == "roles"
    assert User.__tablename__ == "users"
    assert Tenant.__tablename__ == "tenants"
    assert TenantUser.__tablename__ == "tenant_users"
    assert TenantSettings.__tablename__ == "tenant_settings"