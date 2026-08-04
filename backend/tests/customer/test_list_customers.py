from fastapi.testclient import TestClient


def create_customer(
    client: TestClient,
    headers: dict[str, str],
    *,
    first_name: str,
    email: str,
    status: str = "ACTIVE",
    source: str = "WEBSITE",
) -> dict:
    response = client.post(
        "/api/v1/customers/",
        headers=headers,
        json={
            "first_name": first_name,
            "last_name": "Test",
            "email": email,
            "phone": "+919876543210",
            "company": "Test Company",
            "source": source,
            "internal_notes": "Created for list test",
        },
    )

    assert response.status_code == 201, response.text

    customer = response.json()

    if status != "ACTIVE":
        status_response = client.patch(
            f"/api/v1/customers/{customer['id']}/status",
            headers=headers,
            json={"status": status},
        )

        assert status_response.status_code == 200, status_response.text

    return customer


def test_tenant_admin_can_list_customers(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    create_customer(
        client,
        tenant_admin_headers,
        first_name="John",
        email="john.list@test.com",
    )

    create_customer(
        client,
        tenant_admin_headers,
        first_name="Alice",
        email="alice.list@test.com",
    )

    response = client.get(
        "/api/v1/customers/",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 2
    assert data["skip"] == 0
    assert data["limit"] == 20
    assert len(data["items"]) == 2


def test_customer_list_supports_search(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    create_customer(
        client,
        tenant_admin_headers,
        first_name="John",
        email="john.search@test.com",
    )

    create_customer(
        client,
        tenant_admin_headers,
        first_name="Alice",
        email="alice.search@test.com",
    )

    response = client.get(
        "/api/v1/customers/?search=john",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["first_name"] == "John"


def test_customer_list_supports_pagination(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    for index in range(5):
        create_customer(
            client,
            tenant_admin_headers,
            first_name=f"Customer {index}",
            email=f"customer{index}@example.com",
        )

    response = client.get(
        "/api/v1/customers/?skip=1&limit=2",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 5
    assert data["skip"] == 1
    assert data["limit"] == 2
    assert len(data["items"]) == 2


def test_customer_list_filters_by_status(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    create_customer(
        client,
        tenant_admin_headers,
        first_name="Active Customer",
        email="active@test.com",
        status="ACTIVE",
    )

    create_customer(
        client,
        tenant_admin_headers,
        first_name="Blocked Customer",
        email="blocked@test.com",
        status="BLOCKED",
    )

    response = client.get(
        "/api/v1/customers/?customer_status=BLOCKED",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["status"] == "BLOCKED"


def test_customer_list_filters_by_source(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
) -> None:
    create_customer(
        client,
        tenant_admin_headers,
        first_name="Web Customer",
        email="web@test.com",
        source="WEBSITE",
    )

    create_customer(
        client,
        tenant_admin_headers,
        first_name="Phone Customer",
        email="phone@test.com",
        source="PHONE",
    )

    response = client.get(
        "/api/v1/customers/?source=PHONE",
        headers=tenant_admin_headers,
    )

    assert response.status_code == 200, response.text

    data = response.json()

    assert data["total"] == 1
    assert len(data["items"]) == 1
    assert data["items"][0]["source"] == "PHONE"