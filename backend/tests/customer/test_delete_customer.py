from fastapi.testclient import TestClient


def create_customer(
    client: TestClient,
    headers: dict[str, str],
    *,
    email: str = "delete.customer@example.com",
) -> dict:
    response = client.post(
        "/api/v1/customers/",
        headers=headers,
        json={
            "first_name": "Delete",
            "last_name": "Customer",
            "email": email,
            "phone": "+919876543210",
            "company": "Test Company",
            "source": "WEBSITE",
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_tenant_admin_can_delete_customer(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
    )

    response = client.delete(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text
    assert response.json() == {
        "message": "Customer deleted successfully",
    }


def test_deleted_customer_is_no_longer_available(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
        email="deleted.lookup@example.com",
    )

    delete_response = client.delete(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
    )

    assert delete_response.status_code == 200, delete_response.text

    get_response = client.get(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
    )

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Customer not found",
    }


def test_delete_unknown_customer_returns_404(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.delete(
        "/api/v1/customers/999999",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found",
    }


def test_deleted_customer_does_not_appear_in_list(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    first_customer = create_customer(
        client,
        tenant_admin_headers,
        email="first.delete@example.com",
    )

    second_customer = create_customer(
        client,
        tenant_admin_headers,
        email="second.delete@example.com",
    )

    delete_response = client.delete(
        f"/api/v1/customers/{first_customer['id']}",
        headers=tenant_admin_headers,
    )

    assert delete_response.status_code == 200, delete_response.text

    list_response = client.get(
        "/api/v1/customers/",
        headers=tenant_admin_headers,
    )

    assert list_response.status_code == 200, list_response.text

    data = list_response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["id"] == second_customer["id"]