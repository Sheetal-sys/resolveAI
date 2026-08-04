from fastapi.testclient import TestClient


def create_customer(
    client: TestClient,
    headers: dict[str, str],
    *,
    email: str = "status.customer@example.com",
) -> dict:
    response = client.post(
        "/api/v1/customers/",
        headers=headers,
        json={
            "first_name": "Status",
            "last_name": "Customer",
            "email": email,
            "phone": "+919876543210",
            "company": "Test Company",
            "source": "WEBSITE",
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_tenant_admin_can_block_customer(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
    )

    response = client.patch(
        f"/api/v1/customers/{customer['id']}/status",
        headers=tenant_admin_headers,
        json={
            "status": "BLOCKED",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == customer["id"]
    assert data["status"] == "BLOCKED"


def test_customer_status_change_is_persisted(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
        email="persisted.status@example.com",
    )

    update_response = client.patch(
        f"/api/v1/customers/{customer['id']}/status",
        headers=tenant_admin_headers,
        json={
            "status": "INACTIVE",
        },
    )

    assert update_response.status_code == 200, update_response.text

    get_response = client.get(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
    )

    assert get_response.status_code == 200, get_response.text
    assert get_response.json()["status"] == "INACTIVE"


def test_duplicate_customer_status_change_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
        email="duplicate.status@example.com",
    )

    first_response = client.patch(
        f"/api/v1/customers/{customer['id']}/status",
        headers=tenant_admin_headers,
        json={
            "status": "BLOCKED",
        },
    )

    assert first_response.status_code == 200, first_response.text

    second_response = client.patch(
        f"/api/v1/customers/{customer['id']}/status",
        headers=tenant_admin_headers,
        json={
            "status": "BLOCKED",
        },
    )

    assert second_response.status_code == 400
    assert second_response.json() == {
        "detail": "Customer is already BLOCKED",
    }


def test_change_status_for_unknown_customer_returns_404(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.patch(
        "/api/v1/customers/999999/status",
        headers=tenant_admin_headers,
        json={
            "status": "BLOCKED",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found",
    }


def test_invalid_customer_status_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
        email="invalid.status@example.com",
    )

    response = client.patch(
        f"/api/v1/customers/{customer['id']}/status",
        headers=tenant_admin_headers,
        json={
            "status": "SUSPENDED",
        },
    )

    assert response.status_code == 422