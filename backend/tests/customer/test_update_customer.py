from fastapi.testclient import TestClient


def create_customer(
    client: TestClient,
    headers: dict[str, str],
    *,
    email: str = "john.update@example.com",
) -> dict:
    response = client.post(
        "/api/v1/customers/",
        headers=headers,
        json={
            "first_name": "John",
            "last_name": "Smith",
            "email": email,
            "phone": "+919876543210",
            "company": "ABC Ltd",
            "source": "WEBSITE",
            "internal_notes": "Original customer details",
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_tenant_admin_can_update_customer(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
    )

    response = client.patch(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
        json={
            "first_name": "John Updated",
            "phone": "+919999999999",
            "company": "XYZ Ltd",
            "source": "PHONE",
            "internal_notes": "Updated through integration test",
        },
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["id"] == customer["id"]
    assert data["first_name"] == "John Updated"
    assert data["phone"] == "+919999999999"
    assert data["company"] == "XYZ Ltd"
    assert data["source"] == "PHONE"
    assert data["internal_notes"] == (
        "Updated through integration test"
    )

    # Unchanged fields must remain intact.
    assert data["last_name"] == "Smith"
    assert data["email"] == "john.update@example.com"
    assert data["status"] == "ACTIVE"


def test_customer_update_is_persisted(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
        email="persisted.update@example.com",
    )

    update_response = client.patch(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
        json={
            "company": "Persistent Company",
        },
    )

    assert update_response.status_code == 200, update_response.text

    get_response = client.get(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
    )

    assert get_response.status_code == 200, get_response.text
    assert get_response.json()["company"] == "Persistent Company"


def test_update_unknown_customer_returns_404(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    response = client.patch(
        "/api/v1/customers/999999",
        headers=tenant_admin_headers,
        json={
            "company": "Unknown Company",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Customer not found",
    }


def test_empty_customer_update_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    customer = create_customer(
        client,
        tenant_admin_headers,
        email="empty.update@example.com",
    )

    response = client.patch(
        f"/api/v1/customers/{customer['id']}",
        headers=tenant_admin_headers,
        json={},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "No fields were provided for update",
    }


def test_duplicate_customer_email_update_is_rejected(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    first_customer = create_customer(
        client,
        tenant_admin_headers,
        email="first.customer@example.com",
    )

    second_customer = create_customer(
        client,
        tenant_admin_headers,
        email="second.customer@example.com",
    )

    response = client.patch(
        f"/api/v1/customers/{second_customer['id']}",
        headers=tenant_admin_headers,
        json={
            "email": first_customer["email"],
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "A customer with this email already exists",
    }