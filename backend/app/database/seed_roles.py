from app.database.db import SessionLocal
from app.modules.role.models import Role
from app.shared.base.enums import RoleName

DEFAULT_ROLES = [
    {
        "name": RoleName.SUPER_ADMIN.value,
        "description": "ResolveAI platform owner"
    },
    {
        "name": RoleName.TENANT_ADMIN.value,
        "description": "Company admin who manages tenant workspace"
    },
    {
        "name": RoleName.SUPERVISOR.value,
        "description": "Support supervisor"
    },
    {
        "name": RoleName.SUPPORT_AGENT.value,
        "description": "Support agent"
    },
    {
        "name": RoleName.CUSTOMER.value,
        "description": "End customer"
    },
]


def seed_roles():
    db = SessionLocal()

    try:
        for role_data in DEFAULT_ROLES:
            existing_role = db.query(Role).filter(
                Role.name == role_data["name"]
            ).first()

            if not existing_role:
                role = Role(
                    name=role_data["name"],
                    description=role_data["description"]
                )
                db.add(role)

        db.commit()
        print("Default roles seeded successfully.")

    except Exception as e:
        db.rollback()
        print("Error while seeding roles:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()