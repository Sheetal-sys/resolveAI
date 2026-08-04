from fastapi.testclient import TestClient


def create_customer(
    client: TestClient,
    headers: dict[str, str],
):
    response = client.post(
        "/api/v1/customers/",
        headers=headers,
        json={
            "first_name": "John",
            "last_name": "Smith",
            "email": "john.get@test.com",
            "phone": "+919876543210",
            "company": "ABC",
            "source": "WEBSITE",
        },
    )

    assert response.status_code == 201

    return response.json()


def test_get_existing_customer(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
):
    customer = create_customer(
        client,
        tenant_admin_headers,
    )

    response = client.get(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == customer["id"]
    assert data["first_name"] == "John"
    assert data["email"] == "john.get@test.com"


def test_get_unknown_customer(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
):
    response = client.get(
        "/api/v1/customers/999999",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Customer not found"
    }