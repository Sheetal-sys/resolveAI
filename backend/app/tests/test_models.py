from app.modules.role.models import Role
from app.modules.tenant.models import Tenant, TenantUser
from app.modules.user.models import User

print(Role.__tablename__)
print(User.__tablename__)
print(Tenant.__tablename__)
print(TenantUser.__tablename__)