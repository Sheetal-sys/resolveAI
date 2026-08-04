from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.modules.role.models import Role
from app.modules.tenant.models import Tenant, TenantUser
from app.modules.tenant_settings.models import TenantSettings
from app.modules.user.models import User
from app.shared.base.enums import RoleName


TEST_ADMIN_EMAIL = "admin@testshop.com"
TEST_ADMIN_PASSWORD = "Admin@123"

SECOND_ADMIN_EMAIL = "admin@secondshop.com"
SECOND_ADMIN_PASSWORD = "Admin@123"

SUPPORT_AGENT_EMAIL = "agent@testshop.com"
SUPPORT_AGENT_PASSWORD = "Agent@123"

def create_tenant_admin_context(
    db_session: Session,
    *,
    tenant_name: str,
    tenant_slug: str,
    admin_email: str,
    admin_password: str,
    role: Role,
) -> dict[str, Any]:
    tenant = Tenant(
        name=tenant_name,
        slug=tenant_slug,
    )
    db_session.add(tenant)
    db_session.flush()

    admin_user = User(
        first_name=tenant_name,
        last_name="Admin",
        email=admin_email,
        password_hash=hash_password(admin_password),
        is_active=True,
    )
    db_session.add(admin_user)
    db_session.flush()

    tenant_user = TenantUser(
        tenant_id=tenant.id,
        user_id=admin_user.id,
        role_id=role.id,
        is_active=True,
    )
    db_session.add(tenant_user)

    tenant_settings = TenantSettings(
        tenant_id=tenant.id,
    )
    db_session.add(tenant_settings)

    db_session.flush()

    return {
        "tenant": tenant,
        "admin_user": admin_user,
        "tenant_user": tenant_user,
        "role": role,
        "email": admin_email,
        "password": admin_password,
    }


@pytest.fixture()
def tenant_admin_role(
    db_session: Session,
) -> Role:
    role = Role(
        name=RoleName.TENANT_ADMIN.value,
        description="Tenant administrator",
    )

    db_session.add(role)
    db_session.flush()

    return role


@pytest.fixture()
def tenant_admin_context(
    db_session: Session,
    tenant_admin_role: Role,
) -> dict[str, Any]:
    context = create_tenant_admin_context(
        db_session,
        tenant_name="Test Shop",
        tenant_slug="test-shop",
        admin_email=TEST_ADMIN_EMAIL,
        admin_password=TEST_ADMIN_PASSWORD,
        role=tenant_admin_role,
    )

    db_session.commit()

    db_session.refresh(context["tenant"])
    db_session.refresh(context["admin_user"])
    db_session.refresh(context["tenant_user"])

    return context


@pytest.fixture()
def second_tenant_admin_context(
    db_session: Session,
    tenant_admin_role: Role,
) -> dict[str, Any]:
    context = create_tenant_admin_context(
        db_session,
        tenant_name="Second Shop",
        tenant_slug="second-shop",
        admin_email=SECOND_ADMIN_EMAIL,
        admin_password=SECOND_ADMIN_PASSWORD,
        role=tenant_admin_role,
    )

    db_session.commit()

    db_session.refresh(context["tenant"])
    db_session.refresh(context["admin_user"])
    db_session.refresh(context["tenant_user"])

    return context


def login_and_get_token(
    client: TestClient,
    *,
    email: str,
    password: str,
) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200, response.text

    return response.json()["access_token"]


@pytest.fixture()
def tenant_admin_token(
    client: TestClient,
    tenant_admin_context: dict[str, Any],
) -> str:
    return login_and_get_token(
        client,
        email=tenant_admin_context["email"],
        password=tenant_admin_context["password"],
    )


@pytest.fixture()
def second_tenant_admin_token(
    client: TestClient,
    second_tenant_admin_context: dict[str, Any],
) -> str:
    return login_and_get_token(
        client,
        email=second_tenant_admin_context["email"],
        password=second_tenant_admin_context["password"],
    )


@pytest.fixture()
def tenant_admin_headers(
    tenant_admin_token: str,
) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {tenant_admin_token}",
    }


@pytest.fixture()
def second_tenant_admin_headers(
    second_tenant_admin_token: str,
) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {second_tenant_admin_token}",
    }

@pytest.fixture()
def support_agent_role(
    db_session: Session,
) -> Role:
    role = Role(
        name=RoleName.SUPPORT_AGENT.value,
        description="Support agent",
    )

    db_session.add(role)
    db_session.flush()

    return role


@pytest.fixture()
def support_agent_context(
    db_session: Session,
    tenant_admin_context: dict[str, Any],
    support_agent_role: Role,
) -> dict[str, Any]:
    tenant = tenant_admin_context["tenant"]

    agent_user = User(
        first_name="Support",
        last_name="Agent",
        email=SUPPORT_AGENT_EMAIL,
        password_hash=hash_password(SUPPORT_AGENT_PASSWORD),
        is_active=True,
    )

    db_session.add(agent_user)
    db_session.flush()

    tenant_user = TenantUser(
        tenant_id=tenant.id,
        user_id=agent_user.id,
        role_id=support_agent_role.id,
        is_active=True,
    )

    db_session.add(tenant_user)
    db_session.commit()

    db_session.refresh(agent_user)
    db_session.refresh(tenant_user)

    return {
        "tenant": tenant,
        "user": agent_user,
        "tenant_user": tenant_user,
        "role": support_agent_role,
        "email": SUPPORT_AGENT_EMAIL,
        "password": SUPPORT_AGENT_PASSWORD,
    }


@pytest.fixture()
def support_agent_token(
    client: TestClient,
    support_agent_context: dict[str, Any],
) -> str:
    return login_and_get_token(
        client,
        email=support_agent_context["email"],
        password=support_agent_context["password"],
    )


@pytest.fixture()
def support_agent_headers(
    support_agent_token: str,
) -> dict[str, str]:
    return {
        "Authorization": f"Bearer {support_agent_token}",
    }