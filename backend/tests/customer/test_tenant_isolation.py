from fastapi.testclient import TestClient


def create_customer(
    client: TestClient,
    headers: dict[str, str],
    *,
    first_name: str,
    email: str,
) -> dict:
    response = client.post(
        "/api/v1/customers/",
        headers=headers,
        json={
            "first_name": first_name,
            "last_name": "Customer",
            "email": email,
            "phone": "+919876543210",
            "company": "Isolation Test Company",
            "source": "WEBSITE",
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_tenant_cannot_get_another_tenants_customer(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        second_tenant_admin_headers,
        first_name="Second Tenant",
        email="second.get@example.com",
    )

    response = client.get(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found",
    }


def test_tenant_cannot_update_another_tenants_customer(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        second_tenant_admin_headers,
        first_name="Second Tenant",
        email="second.update@example.com",
    )

    response = client.patch(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
        json={
            "company": "Unauthorized Update",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found",
    }


def test_tenant_cannot_change_another_tenants_customer_status(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        second_tenant_admin_headers,
        first_name="Second Tenant",
        email="second.status@example.com",
    )

    response = client.patch(
        f"/api/v1/customers/{customer['id']}/status",
        headers=tenant_admin_headers,
        json={
            "status": "BLOCKED",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found",
    }


def test_tenant_cannot_delete_another_tenants_customer(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        second_tenant_admin_headers,
        first_name="Second Tenant",
        email="second.delete@example.com",
    )

    response = client.delete(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found",
    }


def test_customer_list_contains_only_authenticated_tenant_data(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    second_tenant_admin_headers: dict[str, str],
) -> None:
    create_customer(
        client,
        tenant_admin_headers,
        first_name="First Tenant",
        email="first.list@example.com",
    )

    create_customer(
        client,
        second_tenant_admin_headers,
        first_name="Second Tenant",
        email="second.list@example.com",
    )

    first_response = client.get(
        "/api/v1/customers/",
        headers=tenant_admin_headers,
    )

    second_response = client.get(
        "/api/v1/customers/",
        headers=second_tenant_admin_headers,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200

    first_data = first_response.json()
    second_data = second_response.json()

    assert first_data["total"] == 1
    assert first_data["items"][0]["email"] == "first.list@example.com"

    assert second_data["total"] == 1
    assert second_data["items"][0]["email"] == "second.list@example.com"