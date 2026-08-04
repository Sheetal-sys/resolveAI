from fastapi.testclient import TestClient


def create_customer(
    client: TestClient,
    headers: dict[str, str],
    *,
    email: str,
) -> dict:
    response = client.post(
        "/api/v1/customers/",
        headers=headers,
        json={
            "first_name": "RBAC",
            "last_name": "Customer",
            "email": email,
            "phone": "+919876543210",
            "company": "RBAC Company",
            "source": "WEBSITE",
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_support_agent_can_create_customer(
    client: TestClient,
    support_agent_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/customers/",
        headers=support_agent_headers,
        json={
            "first_name": "Support",
            "last_name": "Created",
            "email": "support.created@example.com",
            "phone": "+919876543210",
            "company": "Support Company",
            "source": "PHONE",
        },
    )

    assert response.status_code == 201, response.text


def test_support_agent_can_list_customers(
    client: TestClient,
    support_agent_headers: dict[str, str],
) -> None:
    create_customer(
        client,
        support_agent_headers,
        email="support.list@example.com",
    )

    response = client.get(
        "/api/v1/customers/",
        headers=support_agent_headers,
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_support_agent_can_view_customer(
    client: TestClient,
    support_agent_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        support_agent_headers,
        email="support.view@example.com",
    )

    response = client.get(
        f"/api/v1/customers/{customer['id']}",
        headers=support_agent_headers,
    )

    assert response.status_code == 200


def test_support_agent_can_update_customer(
    client: TestClient,
    support_agent_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        support_agent_headers,
        email="support.update@example.com",
    )

    response = client.patch(
        f"/api/v1/customers/{customer['id']}",
        headers=support_agent_headers,
        json={
            "company": "Updated by Support Agent",
        },
    )

    assert response.status_code == 200
    assert response.json()["company"] == "Updated by Support Agent"


def test_support_agent_cannot_change_customer_status(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    support_agent_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
        email="support.status@example.com",
    )

    response = client.patch(
        f"/api/v1/customers/{customer['id']}/status",
        headers=support_agent_headers,
        json={
            "status": "BLOCKED",
        },
    )

    assert response.status_code == 403


def test_support_agent_cannot_delete_customer(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    support_agent_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
        email="support.delete@example.com",
    )

    response = client.delete(
        f"/api/v1/customers/{customer['id']}",
        headers=support_agent_headers,
    )

    assert response.status_code == 403


def test_unauthenticated_customer_request_returns_401(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/customers/",
    )

    assert response.status_code == 401