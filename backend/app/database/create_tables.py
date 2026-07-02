from app.database.db import Base, engine

from app.modules.role.models import Role
from app.modules.user.models import User
from app.modules.tenant.models import Tenant, TenantUser

print("Creating ResolveAI database tables...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully.")