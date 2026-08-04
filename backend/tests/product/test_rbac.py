from fastapi.testclient import TestClient


def create_product(
    client: TestClient,
    headers: dict[str, str],
    *,
    sku: str,
) -> dict:
    response = client.post(
        "/api/v1/products/",
        headers=headers,
        json={
            "sku": sku,
            "name": "RBAC Product",
            "description": "Created for RBAC tests",
            "category": "Electronics",
            "brand": "ResolveTech",
            "price": 999.99,
            "currency": "INR",
            "stock_quantity": 10,
        },
    )

    assert response.status_code == 201, response.text

    return response.json()


def test_support_agent_can_list_products(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    support_agent_headers: dict[str, str],
) -> None:
    create_product(
        client,
        tenant_admin_headers,
        sku="RBAC-LIST-001",
    )

    response = client.get(
        "/api/v1/products/",
        headers=support_agent_headers,
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1


def test_support_agent_can_view_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    support_agent_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="RBAC-VIEW-001",
    )

    response = client.get(
        f"/api/v1/products/{product['id']}",
        headers=support_agent_headers,
    )

    assert response.status_code == 200


def test_support_agent_cannot_create_product(
    client: TestClient,
    support_agent_headers: dict[str, str],
) -> None:
    response = client.post(
        "/api/v1/products/",
        headers=support_agent_headers,
        json={
            "sku": "RBAC-CREATE-001",
            "name": "Unauthorized Product",
            "price": 500,
            "currency": "INR",
            "stock_quantity": 5,
        },
    )

    assert response.status_code == 403


def test_support_agent_cannot_update_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    support_agent_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="RBAC-UPDATE-001",
    )

    response = client.patch(
        f"/api/v1/products/{product['id']}",
        headers=support_agent_headers,
        json={
            "name": "Unauthorized Update",
        },
    )

    assert response.status_code == 403


def test_support_agent_cannot_change_product_status(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    support_agent_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="RBAC-STATUS-001",
    )

    response = client.patch(
        f"/api/v1/products/{product['id']}/status",
        headers=support_agent_headers,
        json={
            "status": "INACTIVE",
        },
    )

    assert response.status_code == 403


def test_support_agent_cannot_delete_product(
    client: TestClient,
    tenant_admin_headers: dict[str, str],
    support_agent_headers: dict[str, str],
) -> None:
    product = create_product(
        client,
        tenant_admin_headers,
        sku="RBAC-DELETE-001",
    )

    response = client.delete(
        f"/api/v1/products/{product['id']}",
        headers=support_agent_headers,
    )

    assert response.status_code == 403


def test_unauthenticated_product_request_returns_401(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/v1/products/",
    )

    assert response.status_code == 401